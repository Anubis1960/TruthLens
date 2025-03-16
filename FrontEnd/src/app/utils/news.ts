export interface ArticleStats {
  credible: number;
  misinformation: number;
  political_bias: number;
  unreliable: number;
}

export interface News {
  domain: string;
  articles: { [key: string]: string };  // This represents an object with string keys and values
  stats: ArticleStats;
}