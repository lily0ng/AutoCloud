class Consumer {
  consume(topic: string, handler: (msg: any) => void) {
    console.log(`📥 Consuming from ${topic}`);
    handler({data: 'message'});
  }
}
const consumer = new Consumer();
consumer.consume('events', (msg) => console.log('Received:', msg));
