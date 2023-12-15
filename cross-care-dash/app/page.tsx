import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Card, Title, Text } from '@tremor/react';
import FeaturesSection from '../app/features';
import OpenSourceSection from '../app/open_source';

const IndexPage = () => {
  return (
    <>
      <section className="flex justify-center items-center space-y-6 pb-8 pt-6 md:pb-12 md:pt-10 lg:py-32">
        <div className="flex flex-col items-center text-center max-w-[64rem] w-full gap-4">
          <h1 className="font-heading text-3xl sm:text-5xl md:text-6xl lg:text-7xl">
            Cross-Care Dataset
          </h1>
          <p className="max-w-[42rem] leading-normal text-muted-foreground sm:text-xl sm:leading-8">
            The Cross-Care dataset provides comprehensive insights into
            co-occurrence patterns of various diseases. This dataset is
            invaluable for researchers and healthcare professionals seeking to
            understand complex disease interactions and trends.
          </p>
          <div className="space-x-4">
            <button className="btn mt-4" style={{ flex: '20%' }}>
              <Link href="/tables">Dataset Overview</Link>
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <FeaturesSection />

      {/* Open Source Section */}
      <OpenSourceSection />
    </>
  );
};

export default IndexPage;
