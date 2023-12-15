'use client';

import React, { useState, useEffect } from 'react';
import {
  Card,
  Table,
  TableRow,
  TableCell,
  TableHead,
  TableHeaderCell,
  TableBody,
  Tab,
  TabList,
  TabGroup,
  Select,
  SelectItem
} from '@tremor/react';

const DataCategories = {
  TotalCounts: 'total_counts',
  GenderCounts: 'window_10_gender_subgroup_counts',
  RacialCounts: 'window_10_racial_subgroup_counts'
};

const TablePage = () => {
  const [selectedCategory, setSelectedCategory] = useState(
    DataCategories.TotalCounts
  );
  const [sortKey, setSortKey] = useState('disease');
  const [sortOrder, setSortOrder] = useState('asc'); // Default sort order
  const [dataToShow, setDataToShow] = useState([]);

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

  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 10; // or any other number

  // Function to fetch sorted data from the server
  const fetchSortedData = async () => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/get-sorted-data?category=${selectedCategory}&sortKey=${sortKey}&sortOrder=${sortOrder}&page=${currentPage}&per_page=${pageSize}`
      );
      if (response.ok) {
        const sortedData = await response.json();
        console.log('Fetched Data:', sortedData); // Debugging line
        setDataToShow(sortedData);
        console.log('Updated State:', dataToShow); // To see the updated state
      } else {
        console.error('Server error:', response.status);
      }
    } catch (error) {
      console.error('Network error:', error);
    }
  };

  // Fetch data when sortKey, sortOrder, or selectedCategory changes
  useEffect(() => {
    fetchSortedData();
  }, [selectedCategory, sortKey, sortOrder, currentPage]);

  let displayNames = {};

  if (selectedCategory === DataCategories.TotalCounts) {
    displayNames = totalDisplayNames;
  } else if (selectedCategory === DataCategories.GenderCounts) {
    displayNames = genderDisplayNames;
  } else if (selectedCategory === DataCategories.RacialCounts) {
    displayNames = racialDisplayNames;
  }

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

          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flex: '70%'
            }}
          >
            <Select
              value={sortKey}
              onValueChange={(selectedValue) => {
                const actualKey = displayNames[selectedValue];
                setSortKey(actualKey);
              }}
              style={{ flex: '80%' }}
            >
              {Object.keys(displayNames).map((displayName) => (
                <SelectItem key={displayName} value={displayName}>
                  {displayName}
                </SelectItem>
              ))}
            </Select>{' '}
            <button
              onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
              className={`${'btn'} ${'mt4'}`} /* Apply btn and mt4 class */
              style={{ flex: '20%' }}
            >
              {sortOrder === 'asc' ? 'Ascending' : 'Descending'}
            </button>
          </div>
          <Table className="mt-4">
            <TableHead>
              <TableRow>
                <TableHeaderCell>Disease</TableHeaderCell>
                {selectedCategory === DataCategories.TotalCounts && (
                  <TableHeaderCell className="text-right">
                    Counts
                  </TableHeaderCell>
                )}{' '}
                {selectedCategory === DataCategories.GenderCounts && (
                  <>
                    <TableHeaderCell className="text-right">
                      Male
                    </TableHeaderCell>
                    <TableHeaderCell className="text-right">
                      Female
                    </TableHeaderCell>
                  </>
                )}
                {selectedCategory === DataCategories.RacialCounts && (
                  <>
                    <TableHeaderCell className="text-right">
                      White/Caucasian
                    </TableHeaderCell>
                    <TableHeaderCell className="text-right">
                      Black/African American
                    </TableHeaderCell>
                    <TableHeaderCell className="text-right">
                      Asian
                    </TableHeaderCell>
                    <TableHeaderCell className="text-right">
                      Hispanic/Latino
                    </TableHeaderCell>
                    <TableHeaderCell className="text-right">
                      Pacific Islander
                    </TableHeaderCell>
                    <TableHeaderCell className="text-right">
                      Native American/Indigenous
                    </TableHeaderCell>
                  </>
                )}
              </TableRow>
            </TableHead>
            <TableBody>
              {dataToShow.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.disease}</TableCell>
                  {selectedCategory === DataCategories.TotalCounts && (
                    <TableCell className="text-right">{item['0']}</TableCell>
                  )}
                  {selectedCategory === DataCategories.GenderCounts && (
                    <>
                      <TableCell className="text-right">{item.male}</TableCell>
                      <TableCell className="text-right">
                        {item.female}
                      </TableCell>
                    </>
                  )}
                  {selectedCategory === DataCategories.RacialCounts && (
                    <>
                      <TableCell className="text-right">
                        {item['white/caucasian']}
                      </TableCell>
                      <TableCell className="text-right">
                        {item['black/african american']}
                      </TableCell>
                      <TableCell className="text-right">{item.asian}</TableCell>
                      <TableCell className="text-right">
                        {item['hispanic/latino']}
                      </TableCell>
                      <TableCell className="text-right">
                        {item['pacific islander']}
                      </TableCell>
                      <TableCell className="text-right">
                        {item['native american/indigenous']}
                      </TableCell>
                    </>
                  )}
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <div
            className={'toastContent'}
            style={{ display: 'flex', justifyContent: 'space-between' }}
          >
            <button
              onClick={() => setCurrentPage(currentPage - 1)}
              disabled={currentPage === 1}
              className={`${'btn'} ${'mt4'}`}
            >
              Previous
            </button>
            <span>Page {currentPage}</span>
            <button
              onClick={() => setCurrentPage(currentPage + 1)}
              className={`${'btn'} ${'mt4'}`}
            >
              Next
            </button>
          </div>
        </Card>
      </div>
    </section>
  );
};

export default TablePage;
