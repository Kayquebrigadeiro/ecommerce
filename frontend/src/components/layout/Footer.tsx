'use client';

import Link from 'next/link';
import { GradientText } from '@/components/ui/GradientText';

export function Footer() {
  return (
    <footer className="border-t border-white/10 mt-24">
      <div className="container-custom py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-lg bg-gradient-energy flex items-center justify-center">
                <span className="text-xl">⚡</span>
              </div>
              <span className="text-xl font-bold">
                <GradientText>SportGear</GradientText>
              </span>
            </div>
            <p className="text-text-secondary text-sm">
              Equipamentos de performance para atletas modernos.
            </p>
          </div>

          {/* Links */}
          <div>
            <h3 className="font-semibold text-text-main mb-4">Produtos</h3>
            <ul className="space-y-2 text-sm text-text-secondary">
              <li><Link href="/categorias/futebol" className="hover:text-primary transition-colors">Futebol</Link></li>
              <li><Link href="/categorias/basquete" className="hover:text-primary transition-colors">Basquete</Link></li>
              <li><Link href="/categorias/corrida" className="hover:text-primary transition-colors">Corrida</Link></li>
              <li><Link href="/categorias/academia" className="hover:text-primary transition-colors">Academia</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-text-main mb-4">Suporte</h3>
            <ul className="space-y-2 text-sm text-text-secondary">
              <li><Link href="/contato" className="hover:text-primary transition-colors">Contato</Link></li>
              <li><Link href="/faq" className="hover:text-primary transition-colors">FAQ</Link></li>
              <li><Link href="/trocas" className="hover:text-primary transition-colors">Trocas e Devoluções</Link></li>
            </ul>
          </div>

          <div>
            <h3 className="font-semibold text-text-main mb-4">Legal</h3>
            <ul className="space-y-2 text-sm text-text-secondary">
              <li><Link href="/privacidade" className="hover:text-primary transition-colors">Privacidade</Link></li>
              <li><Link href="/termos" className="hover:text-primary transition-colors">Termos de Uso</Link></li>
            </ul>
          </div>
        </div>

        <div className="mt-12 pt-8 border-t border-white/10 text-center text-sm text-text-secondary">
          <p>&copy; 2026 SportGear Premium. Todos os direitos reservados.</p>
        </div>
      </div>
    </footer>
  );
}
