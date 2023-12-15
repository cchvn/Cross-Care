'use client';

import React, { useState, useEffect } from 'react';
import {
  BarChart,
  Card,
  Title,
  Subtitle,
  Button,
  TabGroup,
  TabList,
  Tab,
  Select,
  SelectItem
} from '@tremor/react';

const DataCategories = {
  TotalCounts: 'total_counts',
  GenderCounts: 'window_10_gender_subgroup_counts',
  RacialCounts: 'window_10_racial_subgroup_counts'
};

const ChartPage = () => {
  const [selectedCategory, setSelectedCategory] = useState(
    DataCategories.TotalCounts
  );
  const [sortKey, setSortKey] = useState('disease');
  const [sortOrder, setSortOrder] = useState('asc');
  const [chartData, setChartData] = useState([]);

  const sortKeys = {
    [DataCategories.TotalCounts]: ['disease', '0'],
    [DataCategories.GenderCounts]: ['disease', 'male', 'female'],
    [DataCategories.RacialCounts]: [
      'disease',
      'white/caucasian',
      'black/african american',
      'asian',
      'hispanic/latino',
      'pacific islander',
      'native american/indigenous'
    ]
  };
  const totalDisplayNames = {
    Disease: 'disease',
    Count: '0'
  };
  const genderDisplayNames = {
    Male: 'male',
    Female: 'female'
  };

  const racialDisplayNames = {
    'White/Caucasian': 'white/caucasian',
    'Black/African American': 'black/african american',
    Asian: 'asian',
    'Hispanic/Latino': 'hispanic/latino',
    'Pacific Islander': 'pacific islander',
    'Native American/Indigenous': 'native american/indigenous'
  };

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await fetch(
          `http://127.0.0.1:5000/get-chart-data?category=${selectedCategory}&sortKey=${sortKey}&sortOrder=${sortOrder}`
        );
        if (response.ok) {
          const fetchedData = await response.json();
          console.log(fetchedData);
          setChartData(fetchedData); // Set transformed data
          console.log(chartData);
        } else {
          console.error('Server error:', response.status);
        }
      } catch (error) {
        console.error('Network error:', error);
      }
    };

    fetchChartData();
  }, [selectedCategory, sortKey, sortOrder]);

  let displayNames = {};

  if (selectedCategory === DataCategories.TotalCounts) {
    displayNames = totalDisplayNames;
  } else if (selectedCategory === DataCategories.GenderCounts) {
    displayNames = genderDisplayNames;
  } else if (selectedCategory === DataCategories.RacialCounts) {
    displayNames = racialDisplayNames;
  }

  // Determine the categories for the BarChart based on the selected category
  let chartCategories = [];
  if (selectedCategory === DataCategories.TotalCounts) {
    chartCategories = ['Total Counts'];
  } else if (selectedCategory === DataCategories.GenderCounts) {
    chartCategories = ['male', 'female'];
  } else if (selectedCategory === DataCategories.RacialCounts) {
    chartCategories = [
      'white/caucasian',
      'black/african american',
      'asian',
      'hispanic/latino',
      'pacific islander',
      'native american/indigenous'
    ];
  }

  const chartColors = [
    'red',
    'blue',
    'green',
    'pink',
    'purple',
    'amber',
    'orange',
    'yellow',
    'brown',
    'grey' // Add more colors as needed
  ];

  return (
    <main className="p-4 md:p-10 mx-auto max-w-7xl">
      <Card>
        <TabGroup
          index={Object.values(DataCategories).indexOf(selectedCategory)}
          onIndexChange={(index) =>
            setSelectedCategory(Object.values(DataCategories)[index])
          }
        >
          <TabList className="mb-4" variant="line">
            <Tab>Total Counts</Tab>
            <Tab>Gender Counts</Tab>
            <Tab>Racial Counts</Tab>
          </TabList>
        </TabGroup>
        <Title>Dynamic Disease Data Visualization</Title>
        <Subtitle>
          Use the controls below to switch between different data
          visualizations.
        </Subtitle>
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center'
          }}
        >
          <Select
            value={sortKey}
            onValueChange={(selectedValue) => {
              const actualKey = displayNames[selectedValue];
              setSortKey(actualKey);
            }}
            style={{ width: '200px' }}
          >
            {Object.keys(displayNames).map((displayName) => (
              <SelectItem key={displayName} value={displayName}>
                {displayName}
              </SelectItem>
            ))}
          </Select>
          <button
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="btn mt-4"
          >
            {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
          </button>
        </div>
        <BarChart
          className="mt-4 h-80"
          data={chartData}
          index="Disease"
          categories={chartCategories}
          colors={chartColors}
          stack={false} // Set to true for stacked bar chart
          yAxisWidth={60}
        />
      </Card>
    </main>
  );
};

export default ChartPage;
