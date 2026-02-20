export interface Product {
  id: number;
  nome: string;
  descricao: string;
  preco: string;
  estoque: number;
  categoria?: string;
  imagem?: string;
  specs?: ProductSpec[];
}

export interface ProductSpec {
  label: string;
  value: string;
}

export interface CartItem {
  id: number;
  produto: number;
  produto_detalhes: Product;
  quantidade: number;
  subtotal: string;
  data_adicionado: string;
}

export interface Cart {
  id: number;
  usuario: number;
  itens: CartItem[];
  total: string;
  total_itens: number;
  data_criacao: string;
  data_atualizacao: string;
}

export interface Order {
  id: number;
  usuario: number;
  usuario_nome: string;
  status: 'pendente' | 'confirmado' | 'enviado' | 'entregue' | 'cancelado';
  total: string;
  data_criacao: string;
  data_atualizacao: string;
  itens: OrderItem[];
}

export interface OrderItem {
  id: number;
  produto: number;
  produto_nome: string;
  quantidade: number;
  preco_unitario: string;
}

export interface Payment {
  id: number;
  pedido: number;
  usuario: number;
  metodo: 'pix' | 'cartao_credito' | 'cartao_debito' | 'boleto';
  status: 'pendente' | 'processando' | 'aprovado' | 'recusado' | 'cancelado';
  valor: string;
  transacao_id?: string;
  codigo_autorizacao?: string;
  data_criacao: string;
  data_aprovacao?: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
}

export interface AuthTokens {
  access: string;
  refresh: string;
}

export interface ApiError {
  error?: string;
  detail?: string;
  message?: string;
}

export type Category = 'futebol' | 'basquete' | 'corrida' | 'academia' | 'lifestyle';

export interface CategoryData {
  id: Category;
  name: string;
  description: string;
  icon: string;
}
