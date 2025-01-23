// Open PDF Viewer in Modal
function openPdfViewer(documentId) {
    const modal = document.getElementById("pdf-viewer-modal");
    const pdfContainer = document.getElementById("pdf-container");

    // Clear any previous PDF rendered
    pdfContainer.innerHTML = "";

    // Fetch the document securely through a view
    fetch(`/serve-pdf/${documentId}/`)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Failed to fetch the PDF.");
            }
            return response.blob();
        })
        .then((blob) => {
            const url = URL.createObjectURL(blob);
            const pdfjsLib = window["pdfjs-dist/build/pdf"];
            pdfjsLib.GlobalWorkerOptions.workerSrc =
                "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js";

            const loadingTask = pdfjsLib.getDocument(url);
            loadingTask.promise.then(
                (pdf) => {
                    // Render first page
                    pdf.getPage(1).then((page) => {
                        const viewport = page.getViewport({ scale: 1.5 });
                        const canvas = document.createElement("canvas");
                        const context = canvas.getContext("2d");
                        canvas.height = viewport.height;
                        canvas.width = viewport.width;

                        // Render the page into the canvas
                        const renderContext = {
                            canvasContext: context,
                            viewport: viewport,
                        };
                        page.render(renderContext);

                        // Append canvas to container
                        pdfContainer.appendChild(canvas);
                    });
                },
                (error) => {
                    console.error(error);
                }
            );
        })
        .catch((error) => {
            alert("Unable to load the document.");
        });

    // Show modal
    modal.style.display = "block";
}

// Close PDF Viewer Modal
function closePdfViewer() {
    const modal = document.getElementById("pdf-viewer-modal");
    modal.style.display = "none";
}
