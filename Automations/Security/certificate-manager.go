package main

import (
	"fmt"
	"log"
	"time"
)

type Certificate struct {
	ID         string
	Domain     string
	Issuer     string
	IssuedAt   time.Time
	ExpiresAt  time.Time
	AutoRenew  bool
}

type CertificateManager struct {
	certificates map[string]*Certificate
}

func NewCertificateManager() *CertificateManager {
	return &CertificateManager{
		certificates: make(map[string]*Certificate),
	}
}

func (cm *CertificateManager) AddCertificate(domain, issuer string, validDays int, autoRenew bool) {
	cert := &Certificate{
		ID:        fmt.Sprintf("cert-%d", len(cm.certificates)+1),
		Domain:    domain,
		Issuer:    issuer,
		IssuedAt:  time.Now(),
		ExpiresAt: time.Now().AddDate(0, 0, validDays),
		AutoRenew: autoRenew,
	}
	
	cm.certificates[cert.ID] = cert
	log.Printf("📜 Certificate added for %s", domain)
}

func (cm *CertificateManager) CheckExpiration() []string {
	expiring := make([]string, 0)
	warningDays := 30
	
	for id, cert := range cm.certificates {
		daysUntilExpiry := int(time.Until(cert.ExpiresAt).Hours() / 24)
		
		if daysUntilExpiry <= warningDays {
			expiring = append(expiring, id)
		}
	}
	
	return expiring
}

func (cm *CertificateManager) RenewCertificate(certID string) error {
	cert, exists := cm.certificates[certID]
	if !exists {
		return fmt.Errorf("certificate not found: %s", certID)
	}
	
	log.Printf("🔄 Renewing certificate for %s", cert.Domain)
	
	cert.IssuedAt = time.Now()
	cert.ExpiresAt = time.Now().AddDate(0, 0, 90)
	
	log.Printf("✅ Certificate renewed, expires: %s", cert.ExpiresAt.Format("2006-01-02"))
	
	return nil
}

func (cm *CertificateManager) AutoRenew() {
	log.Println("🔄 Running automatic certificate renewal...")
	
	expiring := cm.CheckExpiration()
	renewed := 0
	
	for _, certID := range expiring {
		cert := cm.certificates[certID]
		if cert.AutoRenew {
			if err := cm.RenewCertificate(certID); err != nil {
				log.Printf("❌ Failed to renew %s: %v", cert.Domain, err)
			} else {
				renewed++
			}
		}
	}
	
	log.Printf("✅ Renewed %d certificates", renewed)
}

func (cm *CertificateManager) GenerateReport() {
	fmt.Println("\n📜 Certificate Report")
	fmt.Println("====================")
	
	for _, cert := range cm.certificates {
		daysUntilExpiry := int(time.Until(cert.ExpiresAt).Hours() / 24)
		status := "✅"
		
		if daysUntilExpiry <= 30 {
			status = "⚠️"
		}
		if daysUntilExpiry <= 0 {
			status = "❌"
		}
		
		fmt.Printf("%s %s\n", status, cert.Domain)
		fmt.Printf("   Issuer: %s\n", cert.Issuer)
		fmt.Printf("   Expires: %s (%d days)\n", cert.ExpiresAt.Format("2006-01-02"), daysUntilExpiry)
		fmt.Printf("   Auto-renew: %v\n", cert.AutoRenew)
	}
}

func main() {
	manager := NewCertificateManager()
	
	manager.AddCertificate("example.com", "Let's Encrypt", 90, true)
	manager.AddCertificate("api.example.com", "Let's Encrypt", 15, true)
	manager.AddCertificate("old.example.com", "Self-signed", 5, false)
	
	manager.GenerateReport()
	manager.AutoRenew()
}
