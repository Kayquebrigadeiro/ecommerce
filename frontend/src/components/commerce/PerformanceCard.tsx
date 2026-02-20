'use client';

import { Product } from '@/types';
import { HoverLiftCard } from '@/components/motion/HoverLiftCard';
import { Button } from '@/components/ui/Button';
import { useCart } from '@/hooks/useCart';
import { motion } from 'framer-motion';
import Link from 'next/link';

interface PerformanceCardProps {
  product: Product;
}

export function PerformanceCard({ product }: PerformanceCardProps) {
  const { addToCart } = useCart();

  const handleAddToCart = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    addToCart({ produto_id: product.id, quantidade: 1 });
  };

  return (
    <Link href={`/produtos/${product.id}`}>
      <HoverLiftCard className="glass rounded-2xl overflow-hidden group cursor-pointer">
        {/* Image */}
        <div className="relative h-64 bg-gradient-to-br from-surface-light to-surface overflow-hidden">
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="w-32 h-32 rounded-full bg-primary/20 blur-3xl group-hover:bg-primary/30 transition-all duration-cinematic" />
          </div>
          <div className="relative z-10 flex items-center justify-center h-full">
            <span className="text-6xl">🏃</span>
          </div>
          
          {/* Badge */}
          {product.estoque < 10 && product.estoque > 0 && (
            <div className="absolute top-4 right-4 px-3 py-1 rounded-full bg-primary/90 text-white text-xs font-bold">
              Últimas unidades
            </div>
          )}
          
          {product.estoque === 0 && (
            <div className="absolute top-4 right-4 px-3 py-1 rounded-full bg-red-600 text-white text-xs font-bold">
              Esgotado
            </div>
          )}
        </div>

        {/* Content */}
        <div className="p-6">
          <h3 className="text-xl font-bold text-text-main mb-2 group-hover:text-primary transition-colors">
            {product.nome}
          </h3>
          
          <p className="text-text-secondary text-sm mb-4 line-clamp-2">
            {product.descricao}
          </p>

          {/* Price */}
          <div className="flex items-center justify-between mb-4">
            <div>
              <span className="text-3xl font-bold gradient-text">
                R$ {parseFloat(product.preco).toFixed(2)}
              </span>
            </div>
          </div>

          {/* Action */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
          >
            <Button
              variant="energy"
              className="w-full"
              onClick={handleAddToCart}
              disabled={product.estoque === 0}
            >
              {product.estoque === 0 ? 'Indisponível' : 'Adicionar ao Carrinho'}
            </Button>
          </motion.div>
        </div>
      </HoverLiftCard>
    </Link>
  );
}
