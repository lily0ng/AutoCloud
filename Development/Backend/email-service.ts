import nodemailer from 'nodemailer';
import { SESClient, SendEmailCommand } from '@aws-sdk/client-ses';

interface EmailConfig {
  provider: 'smtp' | 'ses';
  smtp?: {
    host: string;
    port: number;
    secure: boolean;
    auth: {
      user: string;
      pass: string;
    };
  };
  ses?: {
    region: string;
    accessKeyId: string;
    secretAccessKey: string;
  };
  from: string;
}

interface EmailMessage {
  to: string | string[];
  subject: string;
  text?: string;
  html?: string;
  cc?: string | string[];
  bcc?: string | string[];
  attachments?: Array<{
    filename: string;
    path?: string;
    content?: string | Buffer;
  }>;
}

export class EmailService {
  private transporter?: nodemailer.Transporter;
  private sesClient?: SESClient;
  private config: EmailConfig;

  constructor(config: EmailConfig) {
    this.config = config;
    this.initialize();
  }

  private initialize(): void {
    if (this.config.provider === 'smtp' && this.config.smtp) {
      this.transporter = nodemailer.createTransport(this.config.smtp);
    } else if (this.config.provider === 'ses' && this.config.ses) {
      this.sesClient = new SESClient({
        region: this.config.ses.region,
        credentials: {
          accessKeyId: this.config.ses.accessKeyId,
          secretAccessKey: this.config.ses.secretAccessKey,
        },
      });
    }
  }

  async sendEmail(message: EmailMessage): Promise<void> {
    if (this.config.provider === 'smtp') {
      await this.sendViaSMTP(message);
    } else if (this.config.provider === 'ses') {
      await this.sendViaSES(message);
    }
  }

  private async sendViaSMTP(message: EmailMessage): Promise<void> {
    if (!this.transporter) {
      throw new Error('SMTP transporter not initialized');
    }

    const mailOptions = {
      from: this.config.from,
      to: Array.isArray(message.to) ? message.to.join(', ') : message.to,
      subject: message.subject,
      text: message.text,
      html: message.html,
      cc: message.cc,
      bcc: message.bcc,
      attachments: message.attachments,
    };

    await this.transporter.sendMail(mailOptions);
  }

  private async sendViaSES(message: EmailMessage): Promise<void> {
    if (!this.sesClient) {
      throw new Error('SES client not initialized');
    }

    const params = {
      Source: this.config.from,
      Destination: {
        ToAddresses: Array.isArray(message.to) ? message.to : [message.to],
        CcAddresses: message.cc ? (Array.isArray(message.cc) ? message.cc : [message.cc]) : undefined,
        BccAddresses: message.bcc ? (Array.isArray(message.bcc) ? message.bcc : [message.bcc]) : undefined,
      },
      Message: {
        Subject: { Data: message.subject },
        Body: {
          Text: message.text ? { Data: message.text } : undefined,
          Html: message.html ? { Data: message.html } : undefined,
        },
      },
    };

    const command = new SendEmailCommand(params);
    await this.sesClient.send(command);
  }

  async verify(): Promise<boolean> {
    if (this.transporter) {
      return await this.transporter.verify();
    }
    return true;
  }
}
