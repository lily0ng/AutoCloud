package main
import ("fmt"; "log")
type Bucket struct {Name string; Region string; Objects int}
func CreateBucket(name, region string) *Bucket {
	bucket := &Bucket{Name: name, Region: region, Objects: 0}
	log.Printf("🪣 Bucket created: %s in %s", name, region)
	return bucket
}
func (b *Bucket) PutObject(key string) {
	b.Objects++
	log.Printf("📤 Object uploaded: %s", key)
}
func main() {
	bucket := CreateBucket("my-bucket", "us-east-1")
	bucket.PutObject("file.txt")
	fmt.Printf("Bucket: %s (%d objects)\n", bucket.Name, bucket.Objects)
}
