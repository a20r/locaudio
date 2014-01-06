Things to do
========

- Create database to store the audio fingerprints
- [x] test

- Create Android app that will do the audio fingerprinting.

    - This should be able to record an arbitrary amount of audio and determine
    the fingerprint from it

    - Use musicg

- Create an easy way for users to add songs to the database to use for recognition

- Create adaptive position determination so we dont have to wait for node events

    - This will reduce the busy wait time which is kind of annoying.

    - Factor in the amount of registered nodes vs the amount that have sent data
    into the probability determination

- Allow nodes to register when they start sending data

