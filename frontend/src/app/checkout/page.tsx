'use client';

import { useState } from 'react';
import { useCart } from '@/hooks/useCart';
import { api } from '@/services/api';
import { Button } from '@/components/ui/Button';
import { GradientText } from '@/components/ui/GradientText';
import { motion } from 'framer-motion';
import { useRouter } from 'next/navigation';

export default function CheckoutPage() {
  const { cart } = useCart();
  const router = useRouter();
  const [isProcessing, setIsProcessing] = useState(false);
  const [metodo, setMetodo] = useState<'pix' | 'cartao_credito' | 'cartao_debito' | 'boleto'>('pix');

  const handleCheckout = async () => {
    if (!cart || cart.itens.length === 0) return;

    setIsProcessing(true);
    try {
      const order = await api.createOrderFromCart();
      const payment = await api.createPayment(order.id, metodo);
      
      router.push(`/pedidos/${order.id}?payment=${payment.id}`);
    } catch (error) {
      console.error('Erro no checkout:', error);
    } finally {
      setIsProcessing(false);
    }
  };

  if (!cart || cart.itens.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">🛒</div>
          <p className="text-text-secondary text-lg mb-4">Seu carrinho está vazio</p>
          <Button onClick={() => router.push('/produtos')}>
            Ver Produtos
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-24">
      <div className="container-custom max-w-4xl">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-4xl font-bold mb-8">
            Finalizar <GradientText>Compra</GradientText>
          </h1>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Resumo */}
            <div className="glass rounded-2xl p-6">
              <h2 className="text-2xl font-bold mb-6">Resumo do Pedido</h2>
              
              <div className="space-y-4 mb-6">
                {cart.itens.map((item) => (
                  <div key={item.id} className="flex justify-between">
                    <div>
                      <p className="font-semibold">{item.produto_detalhes.nome}</p>
                      <p className="text-sm text-text-secondary">Qtd: {item.quantidade}</p>
                    </div>
                    <p className="font-bold">R$ {parseFloat(item.subtotal).toFixed(2)}</p>
                  </div>
                ))}
              </div>

              <div className="border-t border-white/10 pt-4">
                <div className="flex justify-between text-xl font-bold">
                  <span>Total:</span>
                  <span className="gradient-text">R$ {parseFloat(cart.total).toFixed(2)}</span>
                </div>
              </div>
            </div>

            {/* Pagamento */}
            <div className="glass rounded-2xl p-6">
              <h2 className="text-2xl font-bold mb-6">Método de Pagamento</h2>

              <div className="space-y-3 mb-6">
                {[
                  { id: 'pix', label: 'PIX', icon: '⚡' },
                  { id: 'cartao_credito', label: 'Cartão de Crédito', icon: '💳' },
                  { id: 'cartao_debito', label: 'Cartão de Débito', icon: '💳' },
                  { id: 'boleto', label: 'Boleto', icon: '📄' },
                ].map((option) => (
                  <button
                    key={option.id}
                    onClick={() => setMetodo(option.id as any)}
                    className={`w-full p-4 rounded-lg border-2 transition-all ${
                      metodo === option.id
                        ? 'border-primary bg-primary/10'
                        : 'border-white/10 hover:border-white/20'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-2xl">{option.icon}</span>
                      <span className="font-semibold">{option.label}</span>
                    </div>
                  </button>
                ))}
              </div>

              <Button
                variant="energy"
                className="w-full"
                onClick={handleCheckout}
                isLoading={isProcessing}
              >
                Confirmar Pedido
              </Button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
