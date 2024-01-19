'use client';

import React, { useState, useEffect, use } from 'react';
import {
  Card,
  Tab,
  TabList,
  TabGroup,
  Select,
  SelectItem,
  BarChart,
  Title,
  Subtitle,
  Button,
  MultiSelect,
  MultiSelectItem,
  Switch,
  LineChart
} from '@tremor/react';

const DataCategories = {
  TotalCounts: 'total',
  GenderCounts: 'gender',
  RacialCounts: 'racial',
  DrugCounts: 'drug', // need to think about this as many to many
  TimeCounts: 'time'
};

const WindowOptions = {
  Total: 'total',
  Window10: 'window_10',
  Window50: 'window_50',
  Window100: 'window_100',
  Window250: 'window_250'
};

const ChartPage = () => {
  const [selectedCategory, setSelectedCategory] = useState(
    DataCategories.GenderCounts
  );
  const [sortKey, setSortKey] = useState('disease');
  const [sortOrder, setSortOrder] = useState('asc');
  const [dataToShow, setDataToShow] = useState([]);
  const [selectedWindow, setSelectedWindow] = useState(WindowOptions.Total);
  const [selectedDiseases, setSelectedDiseases] = useState([]);
  const [diseaseNames, setDiseaseNames] = useState([]);

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

  const initialDiseaseList = [
    'lupus',
    'mental illness',
    'suicide',
    'ibs',
    'tuberculoses',
    'diabetes',
    'sarcoidoses',
    'pneumonia',
    ' mi ',
    'covid-19',
    'dementia',
    'multiple sclerosis',
    'infection'
  ];

  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10; // or any other number

  const fetchDiseaseNames = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get-disease-names');
      if (response.ok) {
        const names = await response.json();
        setDiseaseNames(names);

        // Set initialDiseases to the diseases from initialDiseaseList that are present in the fetched names
        const initialDiseases = initialDiseaseList.filter((disease) =>
          names.includes(disease)
        );
        setSelectedDiseases(initialDiseases);
      } else {
        console.error('Server error:', response.status);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };
  useEffect(() => {
    fetchDiseaseNames();
  }, []); // Empty dependency array to run only on component mount

  // Function to fetch sorted data from the server
  const fetchChartData = async () => {
    const selectedDiseasesString = selectedDiseases.join(',');
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/get-chart-data?category=${selectedCategory}&selectedWindow=${selectedWindow}&sortKey=${sortKey}&sortOrder=${sortOrder}&page=${currentPage}&per_page=${pageSize}&selectedDiseases=${selectedDiseasesString}`
      );
      if (response.ok) {
        const fetchedData = await response.json();
        setDataToShow(fetchedData); // Set transformed data
      } else {
        console.error('Server error:', response.status);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };

  // Fetch data when sortKey, sortOrder, selectedCategory, or selectedWindow changes
  useEffect(() => {
    fetchChartData();
  }, [
    selectedCategory,
    selectedWindow,
    sortKey,
    sortOrder,
    currentPage,
    selectedDiseases
  ]);

  const [additionalChartData, setAdditionalChartData] = useState([]);

  const fetchAdditionalChartData = async () => {
    const selectedDiseasesString = selectedDiseases.join(',');
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/get-additional-chart-data?category=${selectedCategory}&sortKey=${sortKey}&sortOrder=${sortOrder}&page=${currentPage}&per_page=${pageSize}&selectedDiseases=${selectedDiseasesString}`
      );
      if (response.ok) {
        const fetchedData = await response.json();
        setAdditionalChartData(fetchedData);
        console.log('Additional Chart Data:', additionalChartData);
      } else {
        console.error('Server error:', response.status);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };
  useEffect(() => {
    fetchAdditionalChartData();
  }, [selectedCategory, sortKey, sortOrder, currentPage, selectedDiseases]);

  // Determine display names based on selected category
  let displayNames = {};
  if (selectedCategory === DataCategories.TotalCounts) {
    displayNames = totalDisplayNames;
  } else if (selectedCategory === DataCategories.GenderCounts) {
    displayNames = genderDisplayNames;
  } else if (selectedCategory === DataCategories.RacialCounts) {
    displayNames = racialDisplayNames;
  }

  // Render sort key dropdown options based on the current category
  const renderSortKeyOptions = () => {
    return Object.keys(displayNames).map((displayName) => (
      <SelectItem key={displayName} value={displayNames[displayName]}>
        {displayName}
      </SelectItem>
    ));
  };
  // Determine the categories for the BarChart based on the selected category
  let chartCategories = [];
  if (selectedCategory === DataCategories.TotalCounts) {
    chartCategories = ['0'];
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
    'blue',
    'red',
    'orange',
    'amber',
    'purple',
    'lime',
    'green',
    'pink',
    'emerald',
    'cyan',
    'teal',
    'yellow',
    'zinc',
    'stone',
    'sky',
    'indigo',
    'neutral',
    'violet',
    'slate',
    'fuchsia',
    'rose',
    'gray'
  ];

  return (
    <section className="flex-col justify-center items-center space-y-6 pb-8 pt-6 md:pb-12 md:pt-10 lg:py-32">
      <div className="flex flex-col items-center px-40">
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
          <Subtitle>Counts per disease overall and for each subgroup.</Subtitle>

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flex: '70%'
            }}
          >
            {/* Disease Multiselect */}
            <MultiSelect
              value={selectedDiseases}
              onValueChange={setSelectedDiseases}
              placeholder="Select Diseases"
              style={{ flex: '30%' }}
            >
              {diseaseNames.map((disease) => (
                <MultiSelectItem key={disease} value={disease}>
                  {disease}
                </MultiSelectItem>
              ))}
            </MultiSelect>

            {/* Window Dropdown */}
            <Select
              value={selectedWindow}
              onValueChange={setSelectedWindow}
              style={{ flex: '20%' }}
            >
              {Object.entries(WindowOptions).map(([key, value]) => (
                <SelectItem key={key} value={value}>
                  {key}
                </SelectItem>
              ))}
            </Select>

            {/* Sort Key Dropdown */}
            <Select
              value={sortKey}
              onValueChange={setSortKey}
              style={{ flex: '20%', marginLeft: '20px' }}
            >
              {renderSortKeyOptions()}
            </Select>

            {/* Sort Order Button */}
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="btn mt4"
              style={{ flex: '20%', marginLeft: '20px' }}
            >
              {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            </button>
          </div>
          <BarChart
            className="mt-4 h-80"
            data={dataToShow}
            index="disease"
            categories={chartCategories}
            colors={chartColors}
            stack={false} // Set to true for stacked bar chart
            yAxisWidth={60}
          />
        </Card>
      </div>
      <div className="flex flex-col items-center px-40">
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
          <Title>Relative Representation</Title>
          <Subtitle>
            Percentage difference in counts compared to population census
            estimates.
          </Subtitle>

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flex: '70%'
            }}
          >
            {/* Disease Multiselect */}
            <MultiSelect
              value={selectedDiseases}
              onValueChange={setSelectedDiseases}
              placeholder="Select Diseases"
              style={{ flex: '30%' }}
            >
              {diseaseNames.map((disease) => (
                <MultiSelectItem key={disease} value={disease}>
                  {disease}
                </MultiSelectItem>
              ))}
            </MultiSelect>

            {/* Sort Key Dropdown */}
            <Select
              value={sortKey}
              onValueChange={setSortKey}
              style={{ flex: '20%', marginLeft: '20px' }}
            >
              {renderSortKeyOptions()}
            </Select>

            {/* Sort Order Button */}
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="btn mt4"
              style={{ flex: '20%', marginLeft: '20px' }}
            >
              {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            </button>
          </div>
          <BarChart
            className="mt-4 h-80"
            data={additionalChartData}
            index="disease"
            categories={chartCategories}
            colors={chartColors}
            stack={false} // Set to true for stacked bar chart
            yAxisWidth={60}
          />
        </Card>
      </div>
    </section>
  );
};

export default ChartPage;
