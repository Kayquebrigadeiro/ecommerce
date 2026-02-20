import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import '@/styles/globals.css';
import { Providers } from './providers';
import { Navbar } from '@/components/layout/Navbar';
import { Footer } from '@/components/layout/Footer';
import { CartDrawer } from '@/components/commerce/CartDrawer';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'SportGear Premium - Equipamentos Esportivos de Alta Performance',
  description: 'Equipamentos esportivos de alta performance para atletas modernos',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="pt-BR">
      <body className={inter.className}>
        <Providers>
          <Navbar />
          <main className="min-h-screen pt-20">
            {children}
          </main>
          <Footer />
          <CartDrawer />
        </Providers>
      </body>
    </html>
  );
}
