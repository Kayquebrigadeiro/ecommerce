'use client';

import { useFeaturedProducts } from '@/hooks/useProducts';
import { PerformanceCard } from '@/components/commerce/PerformanceCard';
import { RevealOnScroll } from '@/components/motion/RevealOnScroll';
import { GradientText } from '@/components/ui/GradientText';

export function FeaturedProductsSection() {
  const { data: products, isLoading } = useFeaturedProducts();

  if (isLoading) {
    return (
      <section className="py-24">
        <div className="container-custom">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Produtos em <GradientText>Destaque</GradientText>
            </h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[1, 2, 3, 4, 5, 6].map((i) => (
              <div key={i} className="glass rounded-2xl h-96 animate-pulse" />
            ))}
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-24">
      <div className="container-custom">
        <RevealOnScroll>
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              Produtos em <GradientText>Destaque</GradientText>
            </h2>
            <p className="text-text-secondary text-lg max-w-2xl mx-auto">
              Equipamentos selecionados para máxima performance
            </p>
          </div>
        </RevealOnScroll>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {products?.map((product, index) => (
            <RevealOnScroll key={product.id} delay={index * 0.1}>
              <PerformanceCard product={product} />
            </RevealOnScroll>
          ))}
        </div>
      </div>
    </section>
  );
}
