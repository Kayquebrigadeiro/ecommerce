'use client';

import { ReactNode } from 'react';
import { motion, useInView } from 'framer-motion';
import { useRef } from 'react';

interface RevealOnScrollProps {
  children: ReactNode;
  delay?: number;
  className?: string;
}

export function RevealOnScroll({ children, delay = 0, className = '' }: RevealOnScrollProps) {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: '-100px' });

  return (
    <motion.div
      ref={ref}
      initial={{ opacity: 0, y: 50 }}
      animate={isInView ? { opacity: 1, y: 0 } : { opacity: 0, y: 50 }}
      transition={{ duration: 0.5, delay }}
      className={className}
    >
      {children}
    </motion.div>
  );
}
