'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { useCartStore, useAuthStore } from '@/store';
import { Button } from '@/components/ui/Button';
import { GradientText } from '@/components/ui/GradientText';
import { motion } from 'framer-motion';

export function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const { cart, toggleCart } = useCartStore();
  const { user, isAuthenticated } = useAuthStore();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <motion.nav
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className={`fixed top-0 left-0 right-0 z-30 transition-all duration-cinematic ${
        scrolled ? 'glass-strong py-4' : 'bg-transparent py-6'
      }`}
    >
      <div className="container-custom">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link href="/" className="flex items-center gap-2">
            <div className="w-10 h-10 rounded-lg bg-gradient-energy flex items-center justify-center">
              <span className="text-2xl">⚡</span>
            </div>
            <span className="text-2xl font-bold">
              <GradientText>SportGear</GradientText>
            </span>
          </Link>

          {/* Nav Links */}
          <div className="hidden md:flex items-center gap-8">
            <Link href="/produtos" className="text-text-main hover:text-primary transition-colors">
              Produtos
            </Link>
            <Link href="/categorias" className="text-text-main hover:text-primary transition-colors">
              Categorias
            </Link>
            {isAuthenticated && (
              <Link href="/pedidos" className="text-text-main hover:text-primary transition-colors">
                Meus Pedidos
              </Link>
            )}
          </div>

          {/* Actions */}
          <div className="flex items-center gap-4">
            {/* Cart */}
            <button
              onClick={toggleCart}
              className="relative p-2 rounded-lg hover:bg-surface-light transition-colors"
            >
              <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4M7 13L5.4 5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17m0 0a2 2 0 100 4 2 2 0 000-4zm-8 2a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              {cart && cart.total_itens > 0 && (
                <span className="absolute -top-1 -right-1 w-5 h-5 rounded-full bg-primary text-white text-xs flex items-center justify-center font-bold">
                  {cart.total_itens}
                </span>
              )}
            </button>

            {/* Auth */}
            {isAuthenticated ? (
              <Link href="/perfil">
                <Button variant="ghost" size="sm">
                  {user?.username}
                </Button>
              </Link>
            ) : (
              <Link href="/login">
                <Button variant="primary" size="sm">
                  Entrar
                </Button>
              </Link>
            )}
          </div>
        </div>
      </div>
    </motion.nav>
  );
}
