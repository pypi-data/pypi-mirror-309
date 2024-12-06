"""EPUB file handler implementation"""

from collections.abc import Iterator
from io import BytesIO
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from ebooklib import epub
from PIL import Image
from rich.progress import track

from ..exceptions import FileError
from ..types import (
    Chapter,
    EpubAsset,
    EpubChapter,
    EpubChapterContent,
    EpubImage,
    EpubLink,
    EpubStructure,
    EpubTOC,
    FileContent,
    FileMetadata,
)
from .base import BaseHandler

# Constantes do ebooklib que não estão expostas como atributos
ITEM_DOCUMENT = "document"  # Tipo de item para documentos EPUB


class EPUBHandler(BaseHandler):
    """Enhanced handler for EPUB files"""

    async def read(self, path: Path) -> FileContent:
        """Read EPUB file with enhanced content extraction"""
        try:
            metadata = await self._get_metadata(path)
            book = epub.read_epub(str(path))

            # Extract structured content
            structure = self._extract_structure(book)

            enhanced_metadata = {
                **metadata.metadata,
                "toc": structure.toc,
                "chapters": structure.chapters,
                "assets": structure.assets,
            }

            return FileContent(content=book, metadata=enhanced_metadata, format="epub")
        except Exception as e:
            raise FileError(f"Failed to read EPUB file: {e!s}", cause=e)

    async def analyze_structure(self, book: epub.EpubBook) -> EpubStructure:
        """Analyze EPUB structure and return detailed information"""
        try:
            return self._extract_structure(book)
        except Exception as e:
            raise FileError(f"Failed to analyze EPUB structure: {e!s}", cause=e)

    async def extract_resources(self, book: epub.EpubBook, output_dir: Path) -> None:
        """Extract all resources from EPUB to directory"""
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            images_dir = output_dir / "images"
            chapters_dir = output_dir / "chapters"
            images_dir.mkdir(exist_ok=True)
            chapters_dir.mkdir(exist_ok=True)

            # Extract images
            images = self.extract_images(book)
            for img in track(images, description="Extracting images..."):
                img_path = images_dir / f"{img.identifier}.{img.format or 'unknown'}"
                img_path.write_bytes(img.content)

            # Extract chapters
            for chapter in track(
                self.iter_chapters(book), description="Extracting chapters...",
            ):
                chapter_dir = chapters_dir / self._sanitize_filename(chapter.title)
                chapter_dir.mkdir(exist_ok=True)

                # Save chapter content
                content_file = chapter_dir / "content.html"
                content_file.write_text(chapter.content.html, encoding="utf-8")

                # Save chapter metadata and resources
                self._save_chapter_metadata(chapter_dir, chapter)
                self._save_chapter_resources(chapter_dir, chapter)

        except Exception as e:
            raise FileError(f"Failed to extract EPUB resources: {e!s}", cause=e)

    async def search_content(
        self, book: epub.EpubBook, query: str,
    ) -> list[dict[str, Any]]:
        """Search through EPUB content"""
        try:
            results = []
            for chapter in self.iter_chapters(book):
                # Search in text content
                if query.lower() in chapter.content.text.lower():
                    results.append(
                        {
                            "chapter": chapter.title,
                            "context": self._get_context(chapter.content.text, query),
                            "type": "Text",
                        },
                    )

                # Search in links
                for link in chapter.content.links:
                    if query.lower() in link.text.lower():
                        results.append(
                            {
                                "chapter": chapter.title,
                                "context": f"Link: {link.text} -> {link.href}",
                                "type": "Link",
                            },
                        )

                # Search in image metadata
                for img in chapter.content.images:
                    if any(
                        query.lower() in str(v).lower() for v in img.metadata.values()
                    ):
                        results.append(
                            {
                                "chapter": chapter.title,
                                "context": f"Image: {img.identifier} ({img.metadata.get('alt', '')})",
                                "type": "Image",
                            },
                        )

            return results

        except Exception as e:
            raise FileError(f"Failed to search EPUB content: {e!s}", cause=e)

    def _get_context(self, text: str, query: str, context_size: int = 100) -> str:
        """Get context around search query"""
        idx = text.lower().find(query.lower())
        if idx == -1:
            return ""

        start = max(0, idx - context_size)
        end = min(len(text), idx + len(query) + context_size)

        context = text[start:end]
        if start > 0:
            context = f"...{context}"
        if end < len(text):
            context = f"{context}..."

        return context

    def _sanitize_filename(self, filename: str) -> str:
        """Sanitize filename for filesystem"""
        return "".join(
            c for c in filename if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()

    def _save_chapter_metadata(self, chapter_dir: Path, chapter: EpubChapter) -> None:
        """Save chapter metadata"""
        metadata = {
            "title": chapter.title,
            "order": chapter.order,
            "level": chapter.level,
            "identifier": chapter.identifier,
            "file_name": chapter.file_name,
            "metadata": chapter.metadata,
        }

        metadata_file = chapter_dir / "metadata.json"
        metadata_file.write_text(str(metadata), encoding="utf-8")

    def _save_chapter_resources(self, chapter_dir: Path, chapter: EpubChapter) -> None:
        """Save chapter resources index"""
        resources = {
            "images": [
                {
                    "id": img.identifier,
                    "format": img.format,
                    "dimensions": f"{img.width}x{img.height}"
                    if img.width and img.height
                    else "unknown",
                    "metadata": img.metadata,
                }
                for img in chapter.content.images
            ],
            "links": [
                {
                    "text": link.text,
                    "href": link.href,
                    "type": link.type,
                    "target": link.target,
                }
                for link in chapter.content.links
            ],
            "tables": len(chapter.content.tables),
            "headers": chapter.content.headers,
        }

        resources_file = chapter_dir / "resources.json"
        resources_file.write_text(str(resources), encoding="utf-8")

    def _extract_structure(self, book: epub.EpubBook) -> EpubStructure:
        """Extract complete EPUB structure"""
        # Extract metadata
        metadata = self._extract_metadata(book)

        # Extract assets (images, etc)
        assets = self._extract_assets(book)

        # Extract chapters with enhanced content
        chapters = self._extract_enhanced_chapters(book)

        # Create TOC
        toc = EpubTOC(
            items=[
                Chapter(
                    title=chapter.title,
                    content=chapter.content.html,
                    order=chapter.order,
                    level=chapter.level,
                    identifier=chapter.identifier,
                    metadata=chapter.metadata,
                )
                for chapter in chapters
            ],
        )

        return EpubStructure(
            metadata=metadata, chapters=chapters, assets=assets, toc=toc,
        )

    def _extract_metadata(self, book: epub.EpubBook) -> dict[str, Any]:
        """Extract comprehensive metadata"""
        metadata = {}

        # DC metadata
        dc_fields = [
            "title",
            "creator",
            "subject",
            "description",
            "publisher",
            "contributor",
            "date",
            "type",
            "format",
            "identifier",
            "source",
            "language",
            "relation",
            "coverage",
            "rights",
        ]

        for field in dc_fields:
            values = book.get_metadata("DC", field)
            if values:
                metadata[field] = [v[0] for v in values]

        # Additional metadata
        if book.get_metadata("OPF", "cover"):
            metadata["has_cover"] = True

        return metadata

    def _extract_assets(self, book: epub.EpubBook) -> list[EpubAsset]:
        """Extract all assets from EPUB"""
        assets = []

        for item in book.get_items():
            if isinstance(item, epub.EpubImage):
                # Try to get image dimensions
                try:
                    with BytesIO(item.content) as buf:
                        img = Image.open(buf)
                        width, height = img.size
                        format = img.format.lower() if img.format else None
                except Exception:
                    width = height = None
                    format = None

                image = EpubImage(
                    identifier=str(item.id or f"img_{len(assets)}"),
                    media_type=item.media_type,
                    content=item.content,
                    width=width,
                    height=height,
                    format=format,
                    metadata={
                        "file_name": item.file_name,
                    },
                )
                assets.append(image)
            elif not isinstance(item, epub.EpubHtml):
                # Other assets (audio, etc)
                asset = EpubAsset(
                    identifier=str(item.id or f"asset_{len(assets)}"),
                    media_type=item.media_type,
                    content=item.get_content(),
                    metadata={
                        "file_name": item.file_name,
                    },
                )
                assets.append(asset)

        return assets

    def _extract_enhanced_chapters(self, book: epub.EpubBook) -> list[EpubChapter]:
        """Extract enhanced chapters with structured content"""
        chapters = []
        order = 1

        for item in book.get_items():
            if isinstance(item, epub.EpubHtml):
                # Parse HTML content
                soup = BeautifulSoup(item.content, "lxml")

                # Extract images
                images = []
                for img in soup.find_all("img"):
                    src = img.get("src", "")
                    if src:
                        # Find corresponding image item
                        image_item = next(
                            (
                                i
                                for i in book.get_items()
                                if isinstance(i, epub.EpubImage) and i.file_name == src
                            ),
                            None,
                        )
                        if image_item:
                            try:
                                with BytesIO(image_item.content) as buf:
                                    pil_img = Image.open(buf)
                                    width, height = pil_img.size
                                    format = (
                                        pil_img.format.lower()
                                        if pil_img.format
                                        else None
                                    )
                            except Exception:
                                width = height = None
                                format = None

                            images.append(
                                EpubImage(
                                    identifier=str(
                                        image_item.id or f"img_{len(images)}",
                                    ),
                                    media_type=image_item.media_type,
                                    content=image_item.content,
                                    width=width,
                                    height=height,
                                    format=format,
                                    metadata={
                                        "alt": img.get("alt", ""),
                                        "title": img.get("title", ""),
                                        "file_name": src,
                                    },
                                ),
                            )

                # Extract links
                links = []
                for link in soup.find_all("a"):
                    href = link.get("href", "")
                    if href:
                        parsed = urlparse(href)
                        link_type = (
                            "internal"
                            if not parsed.scheme and not parsed.netloc
                            else "external"
                        )
                        links.append(
                            EpubLink(
                                text=link.get_text(strip=True),
                                href=href,
                                type=link_type,
                                target=link.get("target"),
                            ),
                        )

                # Extract headers
                headers = []
                for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
                    level = int(tag.name[1])
                    headers.append((level, tag.get_text(strip=True)))

                # Create chapter content
                content = EpubChapterContent(
                    html=str(soup),
                    text=soup.get_text(separator="\n\n"),
                    images=images,
                    links=links,
                    tables=[str(t) for t in soup.find_all("table")],
                    headers=headers,
                    metadata={
                        "file_name": item.file_name,
                        "media_type": item.media_type,
                    },
                )

                # Create enhanced chapter
                title = soup.find("title")
                chapter = EpubChapter(
                    title=title.text if title else item.file_name,
                    content=content,
                    order=order,
                    identifier=item.id,
                    file_name=item.file_name,
                    metadata={
                        "media_type": item.media_type,
                    },
                )
                chapters.append(chapter)
                order += 1

        return chapters

    def iter_chapters(self, book: epub.EpubBook) -> Iterator[EpubChapter]:
        """Iterate through chapters"""
        for chapter in self._extract_enhanced_chapters(book):
            yield chapter

    def extract_images(self, book: epub.EpubBook) -> list[EpubImage]:
        """Extract all images from EPUB"""
        return [
            asset
            for asset in self._extract_assets(book)
            if isinstance(asset, EpubImage)
        ]

    def get_chapter_by_id(
        self, book: epub.EpubBook, chapter_id: str,
    ) -> EpubChapter | None:
        """Get specific chapter by ID"""
        return next(
            (
                chapter
                for chapter in self._extract_enhanced_chapters(book)
                if chapter.identifier == chapter_id
            ),
            None,
        )

    async def write(
        self, path: Path, content: Any, metadata: dict[str, Any] | None = None,
    ) -> FileMetadata:
        """Write EPUB file"""
        try:
            if isinstance(content, epub.EpubBook):
                book = content
            else:
                # Create new book if content is dict
                book = epub.EpubBook()

                # Set basic metadata
                if metadata:
                    for key, value in metadata.items():
                        if key in ["title", "language", "identifier"]:
                            setattr(book, key, value)
                        else:
                            book.add_metadata("DC", key, value)

                # Add chapters if provided
                if isinstance(content, dict) and "chapters" in content:
                    for chapter_data in content["chapters"]:
                        chapter = epub.EpubHtml(
                            title=chapter_data.get("title", ""),
                            file_name=chapter_data.get(
                                "file_name",
                                f"chapter_{chapter_data.get('order', 0)}.xhtml",
                            ),
                            content=chapter_data.get("content", ""),
                        )
                        book.add_item(chapter)

                    # Create table of contents usando a constante definida
                    book.toc = [
                        (epub.Section(chapter.title), [chapter])
                        for chapter in book.get_items_of_type(ITEM_DOCUMENT)
                    ]

                    # Add default NCX and Nav files
                    book.add_item(epub.EpubNcx())
                    book.add_item(epub.EpubNav())

                    # Create spine usando a constante definida
                    book.spine = ["nav"] + list(book.get_items_of_type(ITEM_DOCUMENT))

            # Write book to file
            epub.write_epub(str(path), book, {})

            return await self._get_metadata(path)

        except Exception as e:
            raise FileError(f"Failed to write EPUB file: {e!s}", cause=e)
