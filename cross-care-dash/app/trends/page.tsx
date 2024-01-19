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
  LineChart,
  NumberInput,
  CalendarIcon
} from '@tremor/react';

const DataCategories = {
  TotalCounts: 'total',
  TimeCounts: 'time'
};

const WindowOptions = {
  Total: 'total'
};

const TimeOptions = {
  Monthly: 'monthly',
  Yearly: 'yearly',
  Five_Yearly: 'five_yearly'
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

const ChartPage = () => {
  const [selectedCategory, setSelectedCategory] = useState(
    DataCategories.TotalCounts
  );
  const [sortKey, setSortKey] = useState('disease');
  const [sortOrder, setSortOrder] = useState('asc');
  const [selectedWindow, setSelectedWindow] = useState(WindowOptions.Total);
  const [selectedTime, setTime] = useState(TimeOptions.Yearly);
  const [selectedDiseases, setSelectedDiseases] = useState([]);
  const [diseaseNames, setDiseaseNames] = useState([]);
  const [yearStart, setYearStart] = useState(new Date().getFullYear() - 10); // 5 years ago as default
  const [yearEnd, setYearEnd] = useState(new Date().getFullYear()); // Current year as default

  const sortKeys = {
    [DataCategories.TotalCounts]: ['disease', '0']
  };

  const totalDisplayNames = {
    Disease: 'disease',
    Count: '0'
  };

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

  const [temporalChartData, setTemporalChartData] = useState([]);

  const fetchTemporalChartData = async () => {
    const selectedDiseasesString = selectedDiseases.join(',');
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/get-temporal-chart-data?category=${selectedCategory}&timeOption=${selectedTime}&sortKey=${sortKey}&sortOrder=${sortOrder}&startYear=${yearStart}&endYear=${yearEnd}&selectedDiseases=${selectedDiseasesString}`
      );
      if (response.ok) {
        const fetchedData = await response.json();
        setTemporalChartData(fetchedData);
        console.log('Temporal Chart Data:', temporalChartData);
      } else {
        console.error('Server error:', response.status);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };

  useEffect(() => {
    fetchTemporalChartData();
  }, [
    selectedCategory,
    selectedTime,
    sortKey,
    sortOrder,
    currentPage,
    selectedDiseases,
    yearStart,
    yearEnd
  ]);

  const [enableLegendSlider, setEnableLegendSlider] = useState(true); // State to manage legend slider
  // Determine display names based on selected category
  let displayNames = {};
  if (selectedCategory === DataCategories.TotalCounts) {
    displayNames = totalDisplayNames;
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
            </TabList>
          </TabGroup>
          <Title>Representation Trends</Title>
          <Subtitle>Disease counts over time.</Subtitle>
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flex: '70%'
            }}
          >
            {/* Disease MultiSelect with value bound to selectedDiseases */}
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

            {/* Time Option Select */}
            <Select
              value={selectedTime}
              onValueChange={setTime}
              placeholder="Select Time Option"
              style={{ flex: '30%' }}
            >
              {Object.keys(TimeOptions).map((option) => (
                <SelectItem key={option} value={TimeOptions[option]}>
                  {option}
                </SelectItem>
              ))}
            </Select>

            {/* Year Start Input */}
            <NumberInput
              icon={CalendarIcon}
              placeholder="Start Year"
              value={yearStart}
              onChange={(e) => setYearStart(e.target.value)}
              min={2000} // Set minimum year as required
              max={yearEnd} // Maximum is the end year
            />

            {/* Year End Input */}
            <NumberInput
              icon={CalendarIcon}
              placeholder="End Year"
              value={yearEnd}
              onChange={(e) => setYearEnd(e.target.value)}
              min={yearStart} // Minimum is the start year
              max={new Date().getFullYear()} // Set maximum year as the current year
            />

            {/* Sort Order Button */}
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className="btn mt4"
              style={{ flex: '20%', marginLeft: '20px' }}
            >
              {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            </button>
          </div>
          <LineChart
            className="mt-4 h-80"
            data={temporalChartData}
            index="date"
            categories={selectedDiseases}
            colors={chartColors}
            yAxisWidth={60}
            enableLegendSlider={enableLegendSlider} // Use the state here
            showAnimation={true}
          />

          {/* Legend Slider Switch */}
          <div className="p-6 bg-gray-50 border-t flex items-center space-x-3 rounded-b-lg">
            <Switch
              id="legend-slider-switch"
              checked={enableLegendSlider}
              onChange={() => setEnableLegendSlider(!enableLegendSlider)}
            />
            <label
              className="text-sm text-slate-500"
              htmlFor="legend-slider-switch"
            >
              Enable Legend Slider
            </label>
          </div>
        </Card>
      </div>
    </section>
  );
};
export default ChartPage;
