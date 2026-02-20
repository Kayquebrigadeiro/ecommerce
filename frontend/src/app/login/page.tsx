'use client';

import { useState } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { GradientText } from '@/components/ui/GradientText';
import { motion } from 'framer-motion';
import Link from 'next/link';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const { login, isLoading } = useAuth();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    login({ username, password });
  };

  return (
    <div className="min-h-screen flex items-center justify-center py-24">
      <div className="container-custom">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="max-w-md mx-auto"
        >
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold mb-2">
              Bem-vindo de <GradientText>Volta</GradientText>
            </h1>
            <p className="text-text-secondary">Entre para continuar sua jornada</p>
          </div>

          <div className="glass rounded-2xl p-8">
            <form onSubmit={handleSubmit} className="space-y-6">
              <Input
                label="Usuário"
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="seu_usuario"
                required
              />

              <Input
                label="Senha"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
              />

              <Button
                type="submit"
                variant="energy"
                className="w-full"
                isLoading={isLoading}
              >
                Entrar
              </Button>
            </form>

            <div className="mt-6 text-center text-sm text-text-secondary">
              Não tem uma conta?{' '}
              <Link href="/register" className="text-primary hover:underline">
                Criar conta
              </Link>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
