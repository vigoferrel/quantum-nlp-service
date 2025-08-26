const axios = require('axios');

class TestRunner {
  constructor(environmentConfig) {
    this.endpoint = environmentConfig.ENDPOINT;
    this.timeout = environmentConfig.REQUEST_TIMEOUT;
  }

  async run(test, context, constraints) {
    const startTime = Date.now();
    try {
      const response = await axios.post(
        this.endpoint,
        {
          testId: test.id,
          context: context,
          constraints: constraints,
        },
        { timeout: this.timeout }
      );

      return {
        success: true,
        data: response.data,
        latency: Date.now() - startTime,
      };
    } catch (error) {
      return {
        success: false,
        error: this.formatAxiosError(error),
        latency: Date.now() - startTime,
      };
    }
  }

  formatAxiosError(error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      return `Server responded with status ${error.response.status}: ${JSON.stringify(error.response.data)}`;
    } else if (error.request) {
      // The request was made but no response was received
      return `No response received from the server. Message: ${error.message}`;
    } else {
      // Something happened in setting up the request that triggered an Error
      return `Error setting up the request: ${error.message}`;
    }
  }
}

module.exports = TestRunner;
