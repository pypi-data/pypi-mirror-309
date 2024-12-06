/* eslint-disable consistent-return */
/* eslint-disable no-console */
/* eslint-disable import/no-unresolved */
/* eslint-disable import/no-extraneous-dependencies */
const { CognitoIdentityServiceProvider } = require('aws-sdk')

const cognitoIdentityServiceProvider = new CognitoIdentityServiceProvider()

/* This code exports a function named `cognitoResetPassword` that takes an object `userParams` as a
parameter. The function uses the AWS SDK to reset the password of a user in a Cognito user pool. It
sets the new password provided in `userParams`, along with the user pool ID and username. The
`Permanent` parameter is set to `true` to indicate that the user must change their password after
the next login. The function returns an object with a `status` property indicating whether the
password reset was successful, and a `data` property containing the response from the Cognito
service. The function is marked as `async` to allow for the use of `await` when calling the
`adminSetUserPassword` method, which returns a promise. */

module.exports.cognitoResetPassword = async (userParams) => {
    try {
        const params = {
            Password: userParams.password, /* required */
            UserPoolId: process.env.BELINA_ADMIN_COGNITO_USER_POOL_ID, /* required */
            Username: userParams.username, /* required */
            Permanent: true,
        }
        const restPassword = await cognitoIdentityServiceProvider.adminSetUserPassword(params).promise()
        if (restPassword) {
            console.log('success')
            return {
                status: true,
                data: restPassword,
            }
        }
        return {
            status: false,
        }
    } catch (error) {
        throw new Error(error)
    }
}

/* This code exports a function named `updateUserCustomAttributes` that takes two parameters:
`username` and `customAttributes`. The function uses the AWS SDK to update the custom attributes of
a user in a Cognito user pool. It sets the user pool ID and username provided in `username`, along
with the custom attributes provided in `customAttributes`. The function maps the `customAttributes`
array to an array of objects with `Name` and `Value` properties, which are used to update the user's
custom attributes. The function returns nothing, but logs a message to the console indicating
whether the custom attributes were updated successfully or if there was an error. The function is
marked as `async` to allow for the use of `await` when calling the `adminUpdateUserAttributes`
method, which returns a promise. */
module.exports.updateUserCustomAttributes = async (username, customAttributes) => {
    console.log('custom', customAttributes)
    const params = {
        UserPoolId: process.env.BELINA_ADMIN_COGNITO_USER_POOL_ID,
        Username: username,
        UserAttributes: customAttributes.map((attribute) => ({
            Name: attribute.name,
            Value: attribute.value,
        })),
    }
    console.log(params)
    try {
        await cognitoIdentityServiceProvider.adminUpdateUserAttributes(params).promise()
        return { success_status: true }
    } catch (error) {
        console.error('Error updating custom attributes:', error)
        return { success_status: false, message: error.message }
    }
}

/* This code exports a function named `activateDeactivateUser` that takes two parameters: `username`
and `status`. The function uses the AWS SDK to activate or deactivate a user in a Cognito user pool
based on the `status` parameter. It sets the user pool ID and username provided in `username`. The
function determines the appropriate method to call (`adminEnableUser` or `adminDisableUser`) based
on the `status` parameter and calls that method with the provided parameters. The function returns
an object with a `success_status` property indicating whether the operation was successful, and a
`message` property containing an error message if the operation was not successful. The function is
marked as `async` to allow for the use of `await` when calling the `adminEnableUser` or
`adminDisableUser` method, which returns a promise. */
module.exports.activateDeactivateUser = async (username, status) => {
    const params = {
        UserPoolId: process.env.COGNITO_USER_POOL_ID,
        Username: username,
    }
    try {
        const methodName = status ? 'adminEnableUser' : 'adminDisableUser'
        await cognitoIdentityServiceProvider[methodName](params).promise()
        return { success_status: true }
    } catch (error) {
        return { success_status: false, message: error.message }
    }
}

/* This code exports a function named `cognitoUser` that takes a `username` parameter. The function
uses the AWS SDK to retrieve the user attributes of a user in a Cognito user pool. It sets the user
pool ID and username provided in `username`. The function calls the `adminGetUser` method with the
provided parameters and returns an object with a `success_status` property indicating whether the
operation was successful, and a `data` property containing the user attributes if the operation was
successful. If there was an error, the function returns an object with a `success_status` property
set to `false` and a `message` property containing the error message. The function is marked as
`async` to allow for the use of `await` when calling the `adminGetUser` method, which returns a
promise. */
module.exports.cognitoUser = async (username) => {
    const params = {
        UserPoolId: process.env.COGNITO_USER_POOL_ID,
        Username: username,
    }
    try {
        const result = await cognitoIdentityServiceProvider.adminGetUser(params).promise()
        return result.UserAttributes
    } catch (error) {
        console.error('Error:', error)
        return { success_status: false, message: error.message }
    }
}

module.exports.cognitoFindUser = async (username) => {
    const params = {
        UserPoolId: process.env.COGNITO_USER_POOL_ID,
        Username: username,
    }
    try {
        await cognitoIdentityServiceProvider.adminGetUser(params).promise()
        return true // User exists
    } catch (error) {
        if (error.code === 'UserNotFoundException') {
            return false // User doesn't exist
        }
        console.error('Error:', error)
        throw error
    }
}

module.exports.cognitoLoginUser = async (username, password) => {
    console.log('entering...')
    const params = {
        AuthFlow: 'USER_PASSWORD_AUTH',
        ClientId: process.env.COGNITO_CLIENT_ID,
        AuthParameters: {
            USERNAME: username,
            PASSWORD: password,
        },
    }
    try {
        const data = await cognitoIdentityServiceProvider.initiateAuth(params).promise()
        const { AccessToken, IdToken, RefreshToken } = data.AuthenticationResult

        console.log('AccessToken:', AccessToken)
        console.log('IdToken:', IdToken)
        console.log('RefreshToken:', RefreshToken)
        return {
            AccessToken,
            IdToken,
            RefreshToken,
        }
    } catch (error) {
        console.error('Authentication failed:', error)
    }
}
