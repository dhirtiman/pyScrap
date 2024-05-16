import fs from 'fs';
import csvParser from 'csv-parser';
import ExcelJS from 'exceljs';

// Define input and output file paths
const csvFilePath = './CSVtoEx/cin name 6k to 12k (1).csv';
const excelFilePath = './CSVtoEx/cin name 6k to 12k (1).xlsx';

// Function to convert CSV to Excel
async function convertCsvToExcel(csvFilePath, excelFilePath) {
    // Create a new Excel workbook
    const workbook = new ExcelJS.Workbook();

    // Add a new worksheet to the workbook
    const worksheet = workbook.addWorksheet('Sheet 1');

    // Read the CSV file and write data to Excel worksheet
    await new Promise((resolve, reject) => {
        fs.createReadStream(csvFilePath)
            .pipe(csvParser())
            .on('data', (row) => {
                // Convert CSV row to an array of values
                const values = Object.values(row);
                // Add row to Excel worksheet
                worksheet.addRow(values);
            })
            .on('end', () => {
                resolve();
            })
            .on('error', (error) => {
                reject(error);
            });
    });

    // Write the workbook to the Excel file
    await workbook.xlsx.writeFile(excelFilePath);
    console.log(`CSV file ${csvFilePath} converted to Excel file ${excelFilePath}`);
}

// Call the function to convert CSV to Excel
convertCsvToExcel(csvFilePath, excelFilePath)
    .catch((error) => {
        console.error('Error converting CSV to Excel:', error);
    });
