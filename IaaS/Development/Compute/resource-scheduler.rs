use std::collections::VecDeque;

pub struct Task {
    pub id: String,
    pub priority: u8,
}

pub struct Scheduler {
    queue: VecDeque<Task>,
}

impl Scheduler {
    pub fn new() -> Self {
        Scheduler {
            queue: VecDeque::new(),
        }
    }
    
    pub fn schedule(&mut self, task: Task) {
        self.queue.push_back(task);
        println!("📅 Task scheduled: {}", self.queue.back().unwrap().id);
    }
    
    pub fn execute_next(&mut self) -> Option<Task> {
        self.queue.pop_front()
    }
}

fn main() {
    let mut scheduler = Scheduler::new();
    scheduler.schedule(Task { id: "task-1".to_string(), priority: 1 });
    println!("✅ Scheduler ready");
}
