'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface CardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  glow?: boolean;
}

export function Card({ children, className = '', hover = false, glow = false }: CardProps) {
  const Component = hover ? motion.div : 'div';

  return (
    <Component
      className={`glass rounded-xl p-6 ${glow ? 'glow-primary' : ''} ${className}`}
      {...(hover && {
        whileHover: { y: -4, transition: { duration: 0.2 } },
      })}
    >
      {children}
    </Component>
  );
}
