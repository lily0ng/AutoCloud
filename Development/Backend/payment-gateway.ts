import Stripe from 'stripe';

interface PaymentConfig {
  provider: 'stripe';
  stripe?: {
    secretKey: string;
    publishableKey: string;
  };
}

interface PaymentIntent {
  amount: number;
  currency: string;
  customerId?: string;
  description?: string;
  metadata?: Record<string, string>;
}

interface Refund {
  paymentIntentId: string;
  amount?: number;
  reason?: string;
}

export class PaymentGateway {
  private stripeClient?: Stripe;
  private config: PaymentConfig;

  constructor(config: PaymentConfig) {
    this.config = config;
    this.initialize();
  }

  private initialize(): void {
    if (this.config.provider === 'stripe' && this.config.stripe) {
      this.stripeClient = new Stripe(this.config.stripe.secretKey, {
        apiVersion: '2023-10-16',
      });
    }
  }

  async createPaymentIntent(payment: PaymentIntent): Promise<Stripe.PaymentIntent> {
    if (!this.stripeClient) {
      throw new Error('Stripe client not initialized');
    }

    return await this.stripeClient.paymentIntents.create({
      amount: payment.amount,
      currency: payment.currency,
      customer: payment.customerId,
      description: payment.description,
      metadata: payment.metadata,
    });
  }

  async confirmPayment(paymentIntentId: string): Promise<Stripe.PaymentIntent> {
    if (!this.stripeClient) {
      throw new Error('Stripe client not initialized');
    }

    return await this.stripeClient.paymentIntents.confirm(paymentIntentId);
  }

  async refundPayment(refund: Refund): Promise<Stripe.Refund> {
    if (!this.stripeClient) {
      throw new Error('Stripe client not initialized');
    }

    return await this.stripeClient.refunds.create({
      payment_intent: refund.paymentIntentId,
      amount: refund.amount,
      reason: refund.reason as Stripe.RefundCreateParams.Reason,
    });
  }

  async createCustomer(email: string, name?: string): Promise<Stripe.Customer> {
    if (!this.stripeClient) {
      throw new Error('Stripe client not initialized');
    }

    return await this.stripeClient.customers.create({
      email,
      name,
    });
  }

  async getPaymentIntent(id: string): Promise<Stripe.PaymentIntent> {
    if (!this.stripeClient) {
      throw new Error('Stripe client not initialized');
    }

    return await this.stripeClient.paymentIntents.retrieve(id);
  }
}
