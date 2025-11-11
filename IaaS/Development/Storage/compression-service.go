package main
import ("bytes"; "compress/gzip"; "fmt"; "log")
func Compress(data []byte) ([]byte, error) {
	var buf bytes.Buffer
	w := gzip.NewWriter(&buf)
	w.Write(data)
	w.Close()
	log.Printf("🗜️  Compressed: %d -> %d bytes", len(data), buf.Len())
	return buf.Bytes(), nil
}
func main() {
	data := []byte("This is some data to compress")
	compressed, _ := Compress(data)
	fmt.Printf("Compression ratio: %.2f%%\n", float64(len(compressed))/float64(len(data))*100)
}
