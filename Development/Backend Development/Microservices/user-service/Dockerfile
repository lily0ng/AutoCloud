FROM openjdk:11-jre-slim
WORKDIR /app
COPY target/user-service.jar app.jar
EXPOSE 8081
ENTRYPOINT ["java", "-jar", "app.jar"]
