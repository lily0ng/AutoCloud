import { SNSClient, PublishCommand } from '@aws-sdk/client-sns';
import twilio from 'twilio';

interface SMSConfig {
  provider: 'twilio' | 'sns';
  twilio?: {
    accountSid: string;
    authToken: string;
    fromNumber: string;
  };
  sns?: {
    region: string;
    accessKeyId: string;
    secretAccessKey: string;
  };
}

interface SMSMessage {
  to: string;
  body: string;
}

export class SMSService {
  private twilioClient?: twilio.Twilio;
  private snsClient?: SNSClient;
  private config: SMSConfig;

  constructor(config: SMSConfig) {
    this.config = config;
    this.initialize();
  }

  private initialize(): void {
    if (this.config.provider === 'twilio' && this.config.twilio) {
      this.twilioClient = twilio(
        this.config.twilio.accountSid,
        this.config.twilio.authToken
      );
    } else if (this.config.provider === 'sns' && this.config.sns) {
      this.snsClient = new SNSClient({
        region: this.config.sns.region,
        credentials: {
          accessKeyId: this.config.sns.accessKeyId,
          secretAccessKey: this.config.sns.secretAccessKey,
        },
      });
    }
  }

  async sendSMS(message: SMSMessage): Promise<void> {
    if (this.config.provider === 'twilio') {
      await this.sendViaTwilio(message);
    } else if (this.config.provider === 'sns') {
      await this.sendViaSNS(message);
    }
  }

  private async sendViaTwilio(message: SMSMessage): Promise<void> {
    if (!this.twilioClient || !this.config.twilio) {
      throw new Error('Twilio client not initialized');
    }

    await this.twilioClient.messages.create({
      body: message.body,
      from: this.config.twilio.fromNumber,
      to: message.to,
    });
  }

  private async sendViaSNS(message: SMSMessage): Promise<void> {
    if (!this.snsClient) {
      throw new Error('SNS client not initialized');
    }

    const command = new PublishCommand({
      Message: message.body,
      PhoneNumber: message.to,
    });

    await this.snsClient.send(command);
  }

  async sendBulkSMS(messages: SMSMessage[]): Promise<void> {
    await Promise.all(messages.map(msg => this.sendSMS(msg)));
  }
}
