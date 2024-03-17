/*
 * ===============================================================
 * File: document_encryptor.cpp
 * Author: Ari Sohandri Putra
 * E-mail: info.arisohandri@gmail.com
 * Description: This program encrypts or decrypts a Word document using base64 encoding and decoding.
 * ===============================================================
 */
#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include "base64.h"

void encryptDocument(const std::string& documentPath) {
    std::ifstream file(documentPath, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Failed to open file for reading.\n";
        return;
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string plaintext = buffer.str();

    std::string encryptedData = base64_encode(reinterpret_cast<const unsigned char*>(plaintext.c_str()), plaintext.length());

    file.close();

    std::ofstream outFile(documentPath, std::ios::binary);
    if (!outFile.is_open()) {
        std::cerr << "Failed to open file for writing.\n";
        return;
    }

    outFile << encryptedData;
    outFile.close();
}

void decryptDocument(const std::string& documentPath) {
    std::ifstream file(documentPath, std::ios::binary);
    if (!file.is_open()) {
        std::cerr << "Failed to open file for reading.\n";
        return;
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string encryptedData = buffer.str();

    std::string decryptedData = base64_decode(encryptedData);

    file.close();

    std::ofstream outFile(documentPath, std::ios::binary);
    if (!outFile.is_open()) {
        std::cerr << "Failed to open file for writing.\n";
        return;
    }

    outFile << decryptedData;
    outFile.close();
}

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cerr << "Usage: " << argv[0] << " <action> <document_path>\n";
        return 1;
    }

    std::string action = argv[1];
    std::string documentPath = argv[2];

    if (action == "lock") {
        encryptDocument(documentPath);
        std::cout << "File " << documentPath << " encrypted successfully.\n";
    } else if (action == "unlock") {
        decryptDocument(documentPath);
        std::cout << "File " << documentPath << " decrypted successfully.\n";
    } else {
        std::cerr << "Invalid action. Use \"lock\" to encrypt or \"unlock\" to decrypt.\n";
        return 1;
    }

    return 0;
}
