import React from 'react';
import { Card, Text, Flex, Callout, Grid } from '@tremor/react';
import {
  IoAnalyticsSharp,
  IoLanguage,
  IoMedicalOutline
} from 'react-icons/io5';

const features = [
  {
    title: 'Disease Co-occurrence',
    metric: '10,000 Pairs',
    delta: 'Comprehensive Analysis',
    status: 'Data Insights',
    color: 'emerald',
    text: 'Analyzing patterns of disease co-occurrence across demographics.',
    icon: IoAnalyticsSharp
  },
  {
    title: 'NLP Templates',
    metric: 'Disease Prediction',
    delta: 'AI-Driven Analysis',
    status: 'Natural Language Processing',
    color: 'blue',
    text: 'Utilizing NLP templates for insightful health data interpretation.',
    icon: IoLanguage
  },
  {
    title: 'Mechanistic Interpretability',
    metric: 'Colab Demos',
    delta: 'Clarity in Analysis',
    status: 'Interpretability Demos',
    color: 'amber',
    text: 'Demonstrating mechanistic interpretability in healthcare datasets.',
    icon: IoMedicalOutline
  }
];

export default function FeaturesSection() {
  return (
    <section id="features" className="py-8 md:py-12 lg:py-32">
      <div className="text-center max-w-[64rem] mx-auto">
        <h2 className="font-heading text-3xl sm:text-4xl md:text-5xl lg:text-6xl">
          Features
        </h2>
        <p className="max-w-[85%] mx-auto mt-4 text-muted-foreground sm:text-lg md:text-xl">
          Explore the cutting-edge features of our project, showcasing the power
          of data in understanding complex health issues.
        </p>
      </div>

      <Grid
        numItemsSm={2}
        numItemsLg={3}
        className="gap-6 mt-8 mx-auto max-w-[58rem]"
      >
        {features.map((item) => (
          <Card key={item.title}>
            <Text>{item.title}</Text>
            <Flex
              justifyContent="start"
              alignItems="baseline"
              className="space-x-3 truncate"
            >
              <Text className="text-xl font-bold">{item.metric}</Text>
            </Flex>
            <Callout
              className="mt-6"
              title={`${item.status} (${item.delta})`}
              icon={item.icon}
              color={item.color}
            >
              {item.text}
            </Callout>
          </Card>
        ))}
      </Grid>
    </section>
  );
}
