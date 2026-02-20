'use client';

import { motion } from 'framer-motion';
import { Button } from '@/components/ui/Button';
import { GradientText } from '@/components/ui/GradientText';
import Link from 'next/link';

export function HeroPerformance() {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Background Effects */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-secondary/20 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      </div>

      {/* Content */}
      <div className="container-custom relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-6xl md:text-8xl font-bold mb-6">
              Eleve Sua
              <br />
              <GradientText>Performance</GradientText>
            </h1>
          </motion.div>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl md:text-2xl text-text-secondary mb-12 max-w-2xl mx-auto"
          >
            Equipamentos esportivos de alta performance para atletas que buscam excelência.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="flex flex-col sm:flex-row gap-4 justify-center"
          >
            <Link href="/produtos">
              <Button variant="energy" size="lg">
                Explorar Produtos
              </Button>
            </Link>
            <Link href="/categorias">
              <Button variant="outline" size="lg">
                Ver Categorias
              </Button>
            </Link>
          </motion.div>

          {/* Stats */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.6 }}
            className="grid grid-cols-3 gap-8 mt-24 max-w-2xl mx-auto"
          >
            {[
              { value: '500+', label: 'Produtos' },
              { value: '10k+', label: 'Atletas' },
              { value: '98%', label: 'Satisfação' },
            ].map((stat, index) => (
              <div key={index} className="text-center">
                <div className="text-4xl font-bold gradient-text mb-2">{stat.value}</div>
                <div className="text-text-secondary text-sm">{stat.label}</div>
              </div>
            ))}
          </motion.div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 1 }}
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 1.5, repeat: Infinity }}
          className="w-6 h-10 border-2 border-primary rounded-full flex items-start justify-center p-2"
        >
          <div className="w-1 h-2 bg-primary rounded-full" />
        </motion.div>
      </motion.div>
    </section>
  );
}
