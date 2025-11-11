class Producer {
  send(topic: string, message: any) {
    console.log(`📤 Sending to ${topic}:`, message);
  }
}
const producer = new Producer();
producer.send('events', {type: 'user.signup', userId: 123});
