import { Client } from '@elastic/elasticsearch';

interface SearchConfig {
  node: string;
  auth?: {
    username: string;
    password: string;
  };
}

interface IndexDocument {
  index: string;
  id?: string;
  document: Record<string, any>;
}

interface SearchQuery {
  index: string;
  query: Record<string, any>;
  from?: number;
  size?: number;
  sort?: Array<Record<string, any>>;
}

export class SearchEngine {
  private client: Client;

  constructor(config: SearchConfig) {
    this.client = new Client({
      node: config.node,
      auth: config.auth,
    });
  }

  async indexDocument(doc: IndexDocument): Promise<any> {
    return await this.client.index({
      index: doc.index,
      id: doc.id,
      document: doc.document,
    });
  }

  async search(query: SearchQuery): Promise<any> {
    return await this.client.search({
      index: query.index,
      query: query.query,
      from: query.from,
      size: query.size,
      sort: query.sort,
    });
  }

  async deleteDocument(index: string, id: string): Promise<any> {
    return await this.client.delete({
      index,
      id,
    });
  }

  async updateDocument(index: string, id: string, doc: Record<string, any>): Promise<any> {
    return await this.client.update({
      index,
      id,
      doc,
    });
  }

  async bulkIndex(operations: Array<IndexDocument>): Promise<any> {
    const body = operations.flatMap(op => [
      { index: { _index: op.index, _id: op.id } },
      op.document,
    ]);

    return await this.client.bulk({ body });
  }

  async createIndex(index: string, mappings?: Record<string, any>): Promise<any> {
    return await this.client.indices.create({
      index,
      mappings,
    });
  }

  async deleteIndex(index: string): Promise<any> {
    return await this.client.indices.delete({ index });
  }
}
