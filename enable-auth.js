const admin = require('firebase-admin');

admin.initializeApp({
  projectId: 'perception-with-intent'
});

async function enableEmailAuth() {
  try {
    const projectConfig = await admin.auth().updateProjectConfig({
      emailSignIn: {
        enabled: true
      }
    });
    console.log('Email/Password authentication enabled successfully!');
    process.exit(0);
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
}

enableEmailAuth();
