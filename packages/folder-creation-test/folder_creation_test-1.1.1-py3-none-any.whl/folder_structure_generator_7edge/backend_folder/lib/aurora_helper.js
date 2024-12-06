/* eslint-disable no-console */
const Knex = require('knex')

/**
 * The function `initiateKnexConnection` establishes a connection to a PostgreSQL database using the
 * provided environment variables.
 * @returns The function `initiateKnexConnection` returns a Knex instance with the provided connection
 * configuration.
 */
module.exports.initiateKnexConnection = () => {
    const connectionConfig = {
        client: 'pg',
        version: '7.2',
        connection: {
            host: process.env.RDS_CLUSTER_HOST,
            port: 5432,
            user: process.env.RDS_CLUSTER_USERNAME,
            password: process.env.RDS_CLUSTER_PASSWORD,
            database: process.env.RDS_DATABASE_NAME,
            ssl: {
                rejectUnauthorized: false,
            },
        },
    }
    console.log('Aurora Connected Successfully', connectionConfig)
    return Knex(connectionConfig)
}

module.exports.closeKnexConnection = async (knexInstance) => {
    if (knexInstance) {
        await knexInstance.destroy()
        console.log('Aurora Connection Closed Successfully')
    } else {
        console.log('No Knex connection to close')
    }
}

module.exports.auroraFormatListQuery = async (knexData, tableName, query, filterFields, searchFields, extraFields, extraFilter) => {
    // Filter conditions
    if (query.filter) {
        const filterConditions = {}

        filterFields.forEach((param) => {
            if (query[param]) {
                filterConditions[param] = query[param]
            }
        })
        // Condition for filtering by year
        if (extraFilter) {
            if (query.year) {
                knexData.andWhereRaw('EXTRACT(YEAR FROM ??) = ?', [`${tableName}.holiday_date`, query.year])
            }
        }

        if (Object.keys(filterConditions).length > 0) {
            knexData.where(filterConditions)
        }
    }

    // Search conditions
    if (query.search) {
        const trimmedSearch = decodeURIComponent(query.search).trim()
        const search = `%${trimmedSearch.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}%`

        knexData.andWhere((qb) => {
            searchFields.forEach((fieldName) => {
                qb.orWhere(`${tableName}.${fieldName}`, 'ilike', `%${search}%`)
            })
        })
    }

    // any extra fields that can be added using this code
    if (extraFields) {
        knexData.andWhere((qb) => {
            Object.entries(extraFields).forEach(([field, value]) => {
                qb.andWhere(`${tableName}.${field}`, value)
            })
        })
    }
}
