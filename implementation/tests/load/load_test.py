#!/usr/bin/env python3
"""Load Testing Script"""

import time
import requests
import concurrent.futures
from statistics import mean, median

class LoadTester:
    def __init__(self, base_url, num_requests=1000, concurrency=10):
        self.base_url = base_url
        self.num_requests = num_requests
        self.concurrency = concurrency
        self.results = []
    
    def make_request(self):
        """Make a single HTTP request"""
        start = time.time()
        try:
            response = requests.get(f"{self.base_url}/health", timeout=10)
            duration = time.time() - start
            return {
                'status': response.status_code,
                'duration': duration,
                'success': response.status_code == 200
            }
        except Exception as e:
            return {
                'status': 0,
                'duration': time.time() - start,
                'success': False,
                'error': str(e)
            }
    
    def run(self):
        """Run load test"""
        print(f"Starting load test: {self.num_requests} requests with {self.concurrency} concurrent workers")
        
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.concurrency) as executor:
            futures = [executor.submit(self.make_request) for _ in range(self.num_requests)]
            self.results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        total_time = time.time() - start_time
        
        self.print_results(total_time)
    
    def print_results(self, total_time):
        """Print test results"""
        successful = sum(1 for r in self.results if r['success'])
        failed = len(self.results) - successful
        durations = [r['duration'] for r in self.results if r['success']]
        
        print("\n=== Load Test Results ===")
        print(f"Total Requests: {len(self.results)}")
        print(f"Successful: {successful}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {(successful/len(self.results)*100):.2f}%")
        print(f"Total Time: {total_time:.2f}s")
        print(f"Requests/sec: {len(self.results)/total_time:.2f}")
        
        if durations:
            print(f"\nResponse Times:")
            print(f"  Mean: {mean(durations)*1000:.2f}ms")
            print(f"  Median: {median(durations)*1000:.2f}ms")
            print(f"  Min: {min(durations)*1000:.2f}ms")
            print(f"  Max: {max(durations)*1000:.2f}ms")

if __name__ == "__main__":
    tester = LoadTester("http://localhost:8080", num_requests=100, concurrency=10)
    tester.run()
