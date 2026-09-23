export const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10 MB

// Text / email / source code extensions we can read straight as UTF-8 text.
const TEXT_EXTENSIONS = new Set([
  // plain text & data
  "txt",
  "md",
  "csv",
  "tsv",
  "log",
  "json",
  "xml",
  "html",
  "htm",
  "yaml",
  "yml",
  // email (MIME text format)
  "eml",
  // source code
  "js",
  "jsx",
  "ts",
  "tsx",
  "py",
  "java",
  "c",
  "h",
  "cpp",
  "cc",
  "cs",
  "go",
  "rs",
  "php",
  "rb",
  "sh",
  "bash",
  "sql",
  "r",
  "kt",
  "swift",
  "m",
]);

export function getFileExtension(file) {
  const name = file?.name || "";
  const dot = name.lastIndexOf(".");
  return dot === -1 ? "" : name.slice(dot + 1).toLowerCase();
}

export function isSupportedFile(file) {
  const ext = getFileExtension(file);
  return ext === "pdf" || TEXT_EXTENSIONS.has(ext);
}

// Read any supported file to plain text, entirely in the browser.
export async function readFileContent(file) {
  if (!file) throw new Error("No file selected.");

  const ext = getFileExtension(file);

  if (file.size === 0) throw new Error(`"${file.name}" is empty.`);
  if (file.size > MAX_FILE_SIZE) {
    throw new Error(`"${file.name}" is too large (max 10 MB).`);
  }
  if (!isSupportedFile(file)) {
    throw new Error(
      `Unsupported file type${ext ? ` ".${ext}"` : ""}. ` +
        "Supported: text, PDF, email (.eml), and source code files."
    );
  }

  const content = ext === "pdf" ? await readPdfText(file) : await file.text();

  if (!content.trim()) {
    throw new Error(`No readable text found in "${file.name}".`);
  }

  return content.trim();
}

// Extract text from a PDF using PDF.js.
// PDF.js is lazy-loaded so it only hits the bundle when a PDF is actually read.
async function readPdfText(file) {
  const pdfjs = await import("pdfjs-dist");
  const { default: pdfWorkerUrl } = await import(
    "pdfjs-dist/build/pdf.worker.min.mjs?url"
  );
  pdfjs.GlobalWorkerOptions.workerSrc = pdfWorkerUrl;

  const buffer = await file.arrayBuffer();
  const loadingTask = pdfjs.getDocument({ data: buffer });
  const pdf = await loadingTask.promise;

  try {
    let text = "";
    for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
      const page = await pdf.getPage(pageNum);
      const content = await page.getTextContent();

      // Rebuild lines by grouping items that share a similar y position.
      let line = "";
      let lastY = null;
      for (const item of content.items) {
        const y = item.transform?.[5] ?? 0;
        if (lastY !== null && Math.abs(y - lastY) > 2 && line) {
          text += line + "\n";
          line = "";
        }
        line += item.str;
        lastY = y;
      }
      if (line) text += line + "\n";
      text += "\n";
    }
    return text;
  } finally {
    // pdfjs-dist v6 removed PDFDocumentProxy.destroy(); release the worker
    // via the loading task (older versions still accept pdf.destroy()).
    if (typeof pdf.destroy === "function") {
      await pdf.destroy();
    } else {
      await loadingTask.destroy();
    }
  }
}