package main

import (
	"fmt"
	"log"
)

type CDNManager struct {
	distributions map[string]*Distribution
}

type Distribution struct {
	ID      string
	Domain  string
	Origin  string
	Enabled bool
	Caching CacheConfig
}

type CacheConfig struct {
	TTL         int
	QueryString bool
	Cookies     bool
}

func NewCDNManager() *CDNManager {
	return &CDNManager{
		distributions: make(map[string]*Distribution),
	}
}

func (cm *CDNManager) CreateDistribution(domain, origin string) (*Distribution, error) {
	dist := &Distribution{
		ID:      fmt.Sprintf("dist-%d", len(cm.distributions)+1),
		Domain:  domain,
		Origin:  origin,
		Enabled: true,
		Caching: CacheConfig{
			TTL:         3600,
			QueryString: false,
			Cookies:     false,
		},
	}
	
	cm.distributions[dist.ID] = dist
	log.Printf("✅ CDN distribution created: %s", dist.ID)
	
	return dist, nil
}

func (cm *CDNManager) InvalidateCache(distID string, paths []string) error {
	dist, exists := cm.distributions[distID]
	if !exists {
		return fmt.Errorf("distribution not found: %s", distID)
	}
	
	log.Printf("🔄 Invalidating cache for %s", dist.Domain)
	for _, path := range paths {
		log.Printf("   - %s", path)
	}
	
	return nil
}

func (cm *CDNManager) UpdateCacheSettings(distID string, config CacheConfig) error {
	dist, exists := cm.distributions[distID]
	if !exists {
		return fmt.Errorf("distribution not found: %s", distID)
	}
	
	dist.Caching = config
	log.Printf("✅ Cache settings updated for %s", dist.Domain)
	
	return nil
}

func (cm *CDNManager) ListDistributions() {
	fmt.Println("\n📡 CDN Distributions:")
	for _, dist := range cm.distributions {
		status := "Enabled"
		if !dist.Enabled {
			status = "Disabled"
		}
		fmt.Printf("  %s: %s -> %s (%s)\n", dist.ID, dist.Domain, dist.Origin, status)
	}
}

func main() {
	manager := NewCDNManager()
	
	manager.CreateDistribution("cdn.example.com", "origin.example.com")
	manager.CreateDistribution("static.example.com", "s3.amazonaws.com/bucket")
	
	manager.InvalidateCache("dist-1", []string{"/index.html", "/assets/*"})
	
	manager.UpdateCacheSettings("dist-1", CacheConfig{
		TTL:         7200,
		QueryString: true,
		Cookies:     false,
	})
	
	manager.ListDistributions()
}
