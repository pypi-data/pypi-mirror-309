/* eslint-disable no-unused-vars */
/* eslint-disable import/no-extraneous-dependencies */
const {
    config, PinpointEmail,
} = require('aws-sdk')
const knex = require('knex')
const AWS = require('aws-sdk')
const randomNumber = require('random-number')
const ExcelJS = require('exceljs')
const moment = require('moment')

const ses = new AWS.SES()

const pinpoint = new PinpointEmail()
config.update({ region: 'eu-west-1' })

module.exports.generateOtp = async () => {
    const options = {
        min: 100000, max: 999999, integer: true,
    }
    return randomNumber(options)
}

module.exports.convertExcelToJson = async (fileBuffer, headerToObjectMapping) => {
    try {
        const headersMatch = (actualHeaders, expectedHeaders) => JSON.stringify(actualHeaders) === JSON.stringify(expectedHeaders)

        const workbook = new ExcelJS.Workbook()
        try {
            await workbook.xlsx.load(fileBuffer)
        } catch (error) {
            // eslint-disable-next-line no-console
            console.log(error)
            return {
                error: 'invalid_key',
            }
        }

        const worksheet = workbook.getWorksheet(1)
        const totalRows = worksheet?.actualRowCount
        if (totalRows > 101) {
            return {
                error: 'invalid_count',
                totalRows,
            }
        }
        if (totalRows < 2) {
            return {
                error: 'no_record',
                totalRows,
            }
        }

        const excelHeaders = worksheet.getRow(1).values.map((item) => item.trim()).slice(1)
        const objectHeaders = Object.keys(headerToObjectMapping)
        if (!headersMatch(excelHeaders, objectHeaders)) {
            return {
                error: 'invalid_column',
                totalRows,
            }
        }

        const jsonData = []
        await worksheet.eachRow({ includeEmpty: false, includeFormulaValues: true }, (row, rowNumber) => {
            const rowData = {}

            row.eachCell({ includeEmpty: true }, (cell, colNumber) => {
                const headerIndex = colNumber - 1
                const header = excelHeaders[headerIndex]
                if (header) {
                    const propertyName = headerToObjectMapping[header]
                    // const cellValue = typeof cell.value === 'string' && propertyName === 'country'
                    //     ? cell.value.charAt(0).toUpperCase() + cell.value.slice(1).toLowerCase()
                    //     : cell.value

                    rowData[propertyName] = cell.value
                }
            })

            if (rowNumber > 1 && Object.keys(rowData).length > 0) {
                rowData.index = rowNumber
                jsonData.push(rowData)
            }
        })
        return { jsonData, totalRows }
    } catch (error) {
        // eslint-disable-next-line no-console
        console.error('Error:', error.message)// Define a default value for totalRows if it's undefined
        throw error
    }
}

module.exports.getHeaders = () => ({
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Credentials': true,
    'Access-Control-Allow-Headers': '*',
    'Access-Control-Allow-Methods': '*',

})

module.exports.sendSESEmailWithTemplate = async (destinationId, sourceId, templateName, templateData) => {
    const params = {
        Destination: {
            ToAddresses: [destinationId],
        },
        Source: sourceId,
        Template: templateName,
        TemplateData: templateData,
    }
    try {
        const response = await ses.sendTemplatedEmail(params).promise()
        // eslint-disable-next-line no-console
        console.log('Email sent successfully:', response)
        if (response && response.MessageId) {
            return true
        }
        return false
    } catch (error) {
        return false
    }
}

module.exports.sendPinpointEmail = async (destinationId, sourceId, templateData, templateArn) => {
    const params = {
        Content: {
            Template: {
                TemplateArn: templateArn,
                TemplateData: templateData,
            },
        },
        FromEmailAddress: sourceId,
        Destination: {
            ToAddresses: [destinationId],
        },
    }
    try {
        const response = await pinpoint.sendEmail(params).promise()
        // eslint-disable-next-line no-console
        console.log('Email sent successfully:', response)
        if (response && response.MessageId) {
            return true
        }
        return false
    } catch (error) {
        return false
    }
}
