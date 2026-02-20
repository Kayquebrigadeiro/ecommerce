'use client';

import { useCartStore } from '@/store';
import { useCart } from '@/hooks/useCart';
import { motion, AnimatePresence } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { useRouter } from 'next/navigation';

export function CartDrawer() {
  const { isCartOpen, closeCart } = useCartStore();
  const { cart, removeItem, updateItem } = useCart();
  const router = useRouter();

  const handleCheckout = () => {
    closeCart();
    router.push('/checkout');
  };

  return (
    <AnimatePresence>
      {isCartOpen && (
        <>
          {/* Overlay */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeCart}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm z-40"
          />

          {/* Drawer */}
          <motion.div
            initial={{ x: '100%' }}
            animate={{ x: 0 }}
            exit={{ x: '100%' }}
            transition={{ type: 'spring', damping: 30, stiffness: 300 }}
            className="fixed right-0 top-0 h-full w-full max-w-md bg-surface border-l border-white/10 z-50 flex flex-col"
          >
            {/* Header */}
            <div className="p-6 border-b border-white/10">
              <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold gradient-text">Seu Carrinho</h2>
                <button
                  onClick={closeCart}
                  className="text-text-secondary hover:text-text-main transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              {cart && (
                <p className="text-text-secondary text-sm mt-2">
                  {cart.total_itens} {cart.total_itens === 1 ? 'item' : 'itens'}
                </p>
              )}
            </div>

            {/* Items */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-6">
              {!cart || cart.itens.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center">
                  <div className="text-6xl mb-4">🛒</div>
                  <p className="text-text-secondary">Seu carrinho está vazio</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {cart.itens.map((item) => (
                    <motion.div
                      key={item.id}
                      layout
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      exit={{ opacity: 0, x: -20 }}
                      className="glass rounded-lg p-4"
                    >
                      <div className="flex gap-4">
                        <div className="w-20 h-20 rounded-lg bg-surface-light flex items-center justify-center">
                          <span className="text-3xl">🏃</span>
                        </div>
                        
                        <div className="flex-1">
                          <h3 className="font-semibold text-text-main mb-1">
                            {item.produto_detalhes.nome}
                          </h3>
                          <p className="text-primary font-bold">
                            R$ {parseFloat(item.subtotal).toFixed(2)}
                          </p>
                          
                          {/* Quantity Controls */}
                          <div className="flex items-center gap-2 mt-2">
                            <button
                              onClick={() => updateItem({ item_id: item.id, quantidade: Math.max(1, item.quantidade - 1) })}
                              className="w-8 h-8 rounded-md bg-surface-light hover:bg-surface-lighter transition-colors flex items-center justify-center"
                            >
                              -
                            </button>
                            <span className="w-8 text-center font-semibold">{item.quantidade}</span>
                            <button
                              onClick={() => updateItem({ item_id: item.id, quantidade: item.quantidade + 1 })}
                              className="w-8 h-8 rounded-md bg-surface-light hover:bg-surface-lighter transition-colors flex items-center justify-center"
                            >
                              +
                            </button>
                            <button
                              onClick={() => removeItem(item.id)}
                              className="ml-auto text-red-500 hover:text-red-400 transition-colors"
                            >
                              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}
            </div>

            {/* Footer */}
            {cart && cart.itens.length > 0 && (
              <div className="p-6 border-t border-white/10 space-y-4">
                <div className="flex items-center justify-between text-lg">
                  <span className="text-text-secondary">Total:</span>
                  <span className="text-2xl font-bold gradient-text">
                    R$ {parseFloat(cart.total).toFixed(2)}
                  </span>
                </div>
                
                <Button
                  variant="energy"
                  className="w-full"
                  onClick={handleCheckout}
                >
                  Finalizar Compra
                </Button>
              </div>
            )}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}
