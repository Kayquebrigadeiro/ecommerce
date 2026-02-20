'use client';

import { useProducts } from '@/hooks/useProducts';
import { PerformanceCard } from '@/components/commerce/PerformanceCard';
import { GradientText } from '@/components/ui/GradientText';
import { RevealOnScroll } from '@/components/motion/RevealOnScroll';

export default function ProdutosPage() {
  const { data: products, isLoading } = useProducts();

  return (
    <div className="min-h-screen py-24">
      <div className="container-custom">
        <RevealOnScroll>
          <div className="text-center mb-16">
            <h1 className="text-5xl md:text-6xl font-bold mb-4">
              Nossos <GradientText>Produtos</GradientText>
            </h1>
            <p className="text-text-secondary text-lg max-w-2xl mx-auto">
              Equipamentos de alta performance para todos os esportes
            </p>
          </div>
        </RevealOnScroll>

        {isLoading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="glass rounded-2xl h-96 animate-pulse" />
            ))}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {products?.map((product, index) => (
              <RevealOnScroll key={product.id} delay={index * 0.05}>
                <PerformanceCard product={product} />
              </RevealOnScroll>
            ))}
          </div>
        )}

        {!isLoading && products?.length === 0 && (
          <div className="text-center py-24">
            <div className="text-6xl mb-4">📦</div>
            <p className="text-text-secondary text-lg">Nenhum produto encontrado</p>
          </div>
        )}
      </div>
    </div>
  );
}
