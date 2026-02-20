'use client';

import { HeroPerformance } from '@/components/sections/HeroPerformance';
import { FeaturedProductsSection } from '@/components/sections/FeaturedProductsSection';

export default function HomePage() {
  return (
    <>
      <HeroPerformance />
      <FeaturedProductsSection />
    </>
  );
}
