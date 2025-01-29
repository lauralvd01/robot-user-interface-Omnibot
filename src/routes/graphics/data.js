// const firstDataSet = 
//   `title_X,title_Y
//   x-value, y-value
//   x-value, y-value
//   x-value, y-value
//   //insert additional csv data ...
//   `

// const secondDataSet = 
//   `title_X,title_Y
//   x-value, y-value
//   x-value, y-value
//   x-value, y-value
//   //insert additional csv data ...
//   `
 
// const thirdDataSet = 
//   `title_X,title_Y
//   x-value, y-value
//   x-value, y-value
//   x-value, y-value
//   //insert additional csv data ...
//   `
 
// export { firstDataSet, secondDataSet, thirdDataSet };


const csvNortheast = `Year,Population
1920,29.662053
1930,34.427091
1940,35.976777
1950,39.477986
1960,44.677819
1970,49.040703
1980,49.135283
1990,50.809229
2000,53.594378
2010,55.317240
2020,57.609148`;

const csvMidwest = `Year,Population
1920,34.019792
1930,38.594100
1940,40.143332
1950,44.460762
1960,51.619139
1970,56.571663
1980,58.865670
1990,59.668632
2000,64.392776
2010,66.927001
2020,68.985454`;

const csvSouth = `Year,Population
1920,33.125803
1930,37.857633
1940,41.665901
1950,47.197088
1960,54.973113
1970,62.795367
1980,75.372362
1990,85.445930
2000,100.236820
2010,114.555744
2020,126.266107`;

const csvWest = `Year,Population
1920,9.213920
1930,12.323836
1940,14.379119
1950,20.189962
1960,28.053104
1970,34.804193
1980,43.172490
1990,52.786082
2000,63.197932
2010,71.945553
2020,78.588572`;

function csvConvert(csv) {
  return csv.split('\n').slice(1).map(str => {
    const [date, population] = str.split(',')
    .map((el) => (el > 1900 ? new Date(el, 0) : parseFloat(el)));
    return { date, population };
  });
}
const northeast = csvConvert(csvNortheast);
const midwest = csvConvert(csvMidwest);
const south = csvConvert(csvSouth);
const west = csvConvert(csvWest);

// export default [
//   {
//     id: 'Northeast',
//     data: northeast
//   },
//   {
//     id: 'Midwest',
//     data: midwest
//   },
//   {
//     id: 'South',
//     data: south
//   },
//   {
//     id: 'West',
//     data: west
//   }
// ]

const data = [
  {
      "id": "1",
      "data": [
          {
              "date": "2025-01-29T07:57:13.563Z",
              "power_flow": 4.952049864301216
          },
          {
              "date": "2025-01-29T07:57:18.561Z",
              "power_flow": 1.1421121946777362
          },
          {
              "date": "2025-01-29T07:57:23.557Z",
              "power_flow": 2.5697524380249064
          },
          {
              "date": "2025-01-29T07:57:28.563Z",
              "power_flow": -5.781942985556039
          },
          {
              "date": "2025-01-29T07:57:33.563Z",
              "power_flow": -3.0093717175010894
          },
          {
              "date": "2025-01-29T07:57:38.565Z",
              "power_flow": 6.771086364377451
          }
      ]
  },
  {
      "id": "2",
      "data": [
          {
              "date": "2025-01-29T07:57:13.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:18.561Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:23.557Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:28.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:33.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:38.565Z",
              "power_flow": 0
          }
      ]
  },
  {
      "id": "4",
      "data": [
          {
              "date": "2025-01-29T07:57:13.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:18.561Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:23.557Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:28.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:33.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:38.565Z",
              "power_flow": 0
          }
      ]
  },
  {
      "id": "6",
      "data": [
          {
              "date": "2025-01-29T07:57:13.563Z",
              "power_flow": -0.31357345307100104
          },
          {
              "date": "2025-01-29T07:57:18.561Z",
              "power_flow": 0.7055402694097523
          },
          {
              "date": "2025-01-29T07:57:23.557Z",
              "power_flow": 1.5874656061719428
          },
          {
              "date": "2025-01-29T07:57:28.563Z",
              "power_flow": 3.5717976138868712
          },
          {
              "date": "2025-01-29T07:57:33.563Z",
              "power_flow": 9.036544631245459
          },
          {
              "date": "2025-01-29T07:57:38.565Z",
              "power_flow": -3.082225420302282
          }
      ]
  },
  {
      "id": "7",
      "data": [
          {
              "date": "2025-01-29T07:57:13.563Z",
              "power_flow": 2.558412658205498
          },
          {
              "date": "2025-01-29T07:57:18.561Z",
              "power_flow": 5.75642848096237
          },
          {
              "date": "2025-01-29T07:57:23.557Z",
              "power_flow": -2.9519640821653326
          },
          {
              "date": "2025-01-29T07:57:28.563Z",
              "power_flow": 6.641919184871998
          },
          {
              "date": "2025-01-29T07:57:33.563Z",
              "power_flow": 4.944318165961995
          },
          {
              "date": "2025-01-29T07:57:38.565Z",
              "power_flow": -1.1247158734144893
          }
      ]
  },
  {
      "id": "9",
      "data": [
          {
              "date": "2025-01-29T07:57:13.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:18.561Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:23.557Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:28.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:33.563Z",
              "power_flow": 0
          },
          {
              "date": "2025-01-29T07:57:38.565Z",
              "power_flow": 0
          }
      ]
  }
]

const power_infos = [
  {
      "slot_id": 6,
      "name": "Omniwheel on slot 6",
      "power_flow": 3.082225420302282,
      "energy": 42.36751010036096
  },
  {
      "slot_id": 9,
      "name": "Charger on slot 9",
      "power_flow": 0,
      "energy": 0
  },
  {
      "slot_id": 2,
      "name": "Omniwheel on slot 2",
      "power_flow": 0,
      "energy": 5.150145009625703
  },
  {
      "slot_id": 1,
      "name": "Battery on slot 1",
      "power_flow": 6.771086364377451,
      "energy": 4.642944121733308
  },
  {
      "slot_id": 7,
      "name": "Compute on slot 7",
      "power_flow": 1.1247158734144893,
      "energy": 24.511175559833646
  },
  {
      "slot_id": 4,
      "name": "Omniwheel on slot 4",
      "power_flow": 0,
      "energy": 0
  }
]


export default data;