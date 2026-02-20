// Toast simples - pode ser substituído por biblioteca como sonner ou react-hot-toast
export const toast = {
  success: (message: string) => {
    if (typeof window !== 'undefined') {
      console.log('✅', message);
      // Implementar toast visual aqui
    }
  },
  error: (message: string) => {
    if (typeof window !== 'undefined') {
      console.error('❌', message);
      // Implementar toast visual aqui
    }
  },
  info: (message: string) => {
    if (typeof window !== 'undefined') {
      console.info('ℹ️', message);
      // Implementar toast visual aqui
    }
  },
};
