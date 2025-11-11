#!/bin/bash
# Security Log Analyzer

set -e

analyze_auth_logs() {
    echo "🔍 Analyzing authentication logs..."
    
    echo "Failed login attempts:"
    grep "Failed password" /var/log/auth.log | wc -l
    
    echo ""
    echo "Successful logins:"
    grep "Accepted password" /var/log/auth.log | wc -l
    
    echo ""
    echo "Top attacking IPs:"
    grep "Failed password" /var/log/auth.log | \
        awk '{print $(NF-3)}' | \
        sort | uniq -c | sort -rn | head -10
}

analyze_web_logs() {
    echo "🔍 Analyzing web server logs..."
    
    if [ -f /var/log/nginx/access.log ]; then
        echo "Top 10 IPs:"
        awk '{print $1}' /var/log/nginx/access.log | \
            sort | uniq -c | sort -rn | head -10
        
        echo ""
        echo "404 errors:"
        grep " 404 " /var/log/nginx/access.log | wc -l
        
        echo ""
        echo "Suspicious requests:"
        grep -E "(\.\.\/|union|select|script)" /var/log/nginx/access.log | tail -10
    fi
}

detect_brute_force() {
    echo "🔍 Detecting brute force attempts..."
    
    local threshold=10
    
    awk '/Failed password/ {print $(NF-3)}' /var/log/auth.log | \
        sort | uniq -c | sort -rn | \
        awk -v threshold="$threshold" '$1 > threshold {print "⚠️  " $2 " - " $1 " attempts"}'
}

check_privilege_escalation() {
    echo "🔍 Checking for privilege escalation attempts..."
    
    grep "sudo" /var/log/auth.log | grep -E "(FAILED|incorrect password)" | tail -20
}

generate_security_report() {
    local report_file="/var/log/security-report-$(date +%Y%m%d).txt"
    
    echo "📊 Generating security report..."
    
    {
        echo "Security Report - $(date)"
        echo "=========================="
        echo ""
        
        echo "Authentication Summary:"
        analyze_auth_logs
        
        echo ""
        echo "Brute Force Detection:"
        detect_brute_force
        
        echo ""
        echo "Privilege Escalation Attempts:"
        check_privilege_escalation
        
    } > "$report_file"
    
    echo "✅ Report saved to: $report_file"
}

case "${1:-report}" in
    auth)
        analyze_auth_logs
        ;;
    web)
        analyze_web_logs
        ;;
    brute-force)
        detect_brute_force
        ;;
    escalation)
        check_privilege_escalation
        ;;
    report)
        generate_security_report
        ;;
esac
