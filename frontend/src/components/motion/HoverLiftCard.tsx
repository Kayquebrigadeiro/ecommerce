'use client';

import { ReactNode } from 'react';
import { motion } from 'framer-motion';

interface HoverLiftCardProps {
  children: ReactNode;
  className?: string;
}

export function HoverLiftCard({ children, className = '' }: HoverLiftCardProps) {
  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ duration: 0.24 }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
