class DataGenerator {
  static generateFor(test) {
    switch (test.id) {
      case 'full_monorepo_audit_750k':
        return { context: 'a'.repeat(test.totalTokenSize) };

      case 'iops_stress_test_10k_files': {
        const files = {};
        const tokensPerFile = Math.floor(test.totalTokenSize / test.fileCount);
        for (let i = 0; i < test.fileCount; i++) {
          files[`file_${i}.txt`] = 'b'.repeat(tokensPerFile);
        }
        return { context: JSON.stringify(files) };
      }

      case 'db_connection_pressure_test':
        return {
          context: 'c'.repeat(test.totalTokenSize),
          parallelQueries: test.parallelQueries
        };

      default:
        console.warn(`Warning: No data generation strategy found for test ID: ${test.id}`);
        return { context: '' };
    }
  }
}

module.exports = DataGenerator;
