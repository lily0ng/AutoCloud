use std::collections::HashMap;
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};

#[derive(Clone)]
pub struct RateLimiter {
    limits: Arc<Mutex<HashMap<String, ClientLimit>>>,
    max_requests: usize,
    window: Duration,
}

struct ClientLimit {
    requests: Vec<Instant>,
}

impl RateLimiter {
    pub fn new(max_requests: usize, window_secs: u64) -> Self {
        RateLimiter {
            limits: Arc::new(Mutex::new(HashMap::new())),
            max_requests,
            window: Duration::from_secs(window_secs),
        }
    }

    pub fn check_rate_limit(&self, client_id: &str) -> Result<(), String> {
        let mut limits = self.limits.lock().unwrap();
        let now = Instant::now();

        let client_limit = limits
            .entry(client_id.to_string())
            .or_insert(ClientLimit {
                requests: Vec::new(),
            });

        // Remove expired requests
        client_limit
            .requests
            .retain(|&time| now.duration_since(time) < self.window);

        if client_limit.requests.len() >= self.max_requests {
            return Err(format!("Rate limit exceeded for client: {}", client_id));
        }

        client_limit.requests.push(now);
        Ok(())
    }

    pub fn reset(&self, client_id: &str) {
        let mut limits = self.limits.lock().unwrap();
        limits.remove(client_id);
    }

    pub fn cleanup_expired(&self) {
        let mut limits = self.limits.lock().unwrap();
        let now = Instant::now();

        limits.retain(|_, client_limit| {
            client_limit
                .requests
                .retain(|&time| now.duration_since(time) < self.window);
            !client_limit.requests.is_empty()
        });
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread;

    #[test]
    fn test_rate_limiting() {
        let limiter = RateLimiter::new(5, 60);

        for _ in 0..5 {
            assert!(limiter.check_rate_limit("client1").is_ok());
        }

        assert!(limiter.check_rate_limit("client1").is_err());
    }

    #[test]
    fn test_different_clients() {
        let limiter = RateLimiter::new(2, 60);

        assert!(limiter.check_rate_limit("client1").is_ok());
        assert!(limiter.check_rate_limit("client2").is_ok());
        assert!(limiter.check_rate_limit("client1").is_ok());
        assert!(limiter.check_rate_limit("client2").is_ok());
    }
}
