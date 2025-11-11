package main

import (
	"fmt"
	"io"
	"log"
	"mime/multipart"
	"net/http"
	"os"
	"path/filepath"
	"strings"

	"github.com/google/uuid"
)

const (
	MaxUploadSize = 10 << 20 // 10 MB
	UploadPath    = "./uploads"
)

type FileUploadService struct {
	uploadPath string
	maxSize    int64
}

func NewFileUploadService(uploadPath string, maxSize int64) *FileUploadService {
	os.MkdirAll(uploadPath, os.ModePerm)
	return &FileUploadService{
		uploadPath: uploadPath,
		maxSize:    maxSize,
	}
}

func (s *FileUploadService) UploadHandler(w http.ResponseWriter, r *http.Request) {
	r.Body = http.MaxBytesReader(w, r.Body, s.maxSize)
	
	if err := r.ParseMultipartForm(s.maxSize); err != nil {
		http.Error(w, "File too large", http.StatusBadRequest)
		return
	}

	file, header, err := r.FormFile("file")
	if err != nil {
		http.Error(w, "Error retrieving file", http.StatusBadRequest)
		return
	}
	defer file.Close()

	filename := s.generateFilename(header.Filename)
	filepath := filepath.Join(s.uploadPath, filename)

	dst, err := os.Create(filepath)
	if err != nil {
		http.Error(w, "Error saving file", http.StatusInternalServerError)
		return
	}
	defer dst.Close()

	if _, err := io.Copy(dst, file); err != nil {
		http.Error(w, "Error saving file", http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, "File uploaded successfully: %s", filename)
}

func (s *FileUploadService) generateFilename(original string) string {
	ext := filepath.Ext(original)
	return uuid.New().String() + ext
}

func main() {
	service := NewFileUploadService(UploadPath, MaxUploadSize)
	http.HandleFunc("/upload", service.UploadHandler)
	log.Println("File upload server running on :8080")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
