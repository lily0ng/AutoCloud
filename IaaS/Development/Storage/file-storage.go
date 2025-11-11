package main
import ("fmt"; "log")
type FileSystem struct {ID string; Size int; MountPoint string}
func CreateFileSystem(size int, mount string) *FileSystem {
	fs := &FileSystem{ID: fmt.Sprintf("fs-%d", size), Size: size, MountPoint: mount}
	log.Printf("📁 File system created: %s mounted at %s", fs.ID, mount)
	return fs
}
func main() {
	fs := CreateFileSystem(500, "/mnt/data")
	fmt.Printf("FileSystem: %s - %dGB at %s\n", fs.ID, fs.Size, fs.MountPoint)
}
