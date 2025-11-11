package main

import (
	"encoding/json"
	"log"
	"net/http"

	"github.com/graphql-go/graphql"
	"github.com/graphql-go/handler"
)

// User type definition
type User struct {
	ID    string `json:"id"`
	Name  string `json:"name"`
	Email string `json:"email"`
}

// Mock data store
var users = []User{
	{ID: "1", Name: "John Doe", Email: "john@example.com"},
	{ID: "2", Name: "Jane Smith", Email: "jane@example.com"},
}

// GraphQL User Type
var userType = graphql.NewObject(
	graphql.ObjectConfig{
		Name: "User",
		Fields: graphql.Fields{
			"id": &graphql.Field{
				Type: graphql.String,
			},
			"name": &graphql.Field{
				Type: graphql.String,
			},
			"email": &graphql.Field{
				Type: graphql.String,
			},
		},
	},
)

// Root Query
var rootQuery = graphql.NewObject(
	graphql.ObjectConfig{
		Name: "RootQuery",
		Fields: graphql.Fields{
			"user": &graphql.Field{
				Type:        userType,
				Description: "Get user by ID",
				Args: graphql.FieldConfigArgument{
					"id": &graphql.ArgumentConfig{
						Type: graphql.String,
					},
				},
				Resolve: func(params graphql.ResolveParams) (interface{}, error) {
					id, ok := params.Args["id"].(string)
					if ok {
						for _, user := range users {
							if user.ID == id {
								return user, nil
							}
						}
					}
					return nil, nil
				},
			},
			"users": &graphql.Field{
				Type:        graphql.NewList(userType),
				Description: "Get all users",
				Resolve: func(params graphql.ResolveParams) (interface{}, error) {
					return users, nil
				},
			},
		},
	},
)

// Root Mutation
var rootMutation = graphql.NewObject(
	graphql.ObjectConfig{
		Name: "RootMutation",
		Fields: graphql.Fields{
			"createUser": &graphql.Field{
				Type:        userType,
				Description: "Create a new user",
				Args: graphql.FieldConfigArgument{
					"name": &graphql.ArgumentConfig{
						Type: graphql.NewNonNull(graphql.String),
					},
					"email": &graphql.ArgumentConfig{
						Type: graphql.NewNonNull(graphql.String),
					},
				},
				Resolve: func(params graphql.ResolveParams) (interface{}, error) {
					name, _ := params.Args["name"].(string)
					email, _ := params.Args["email"].(string)
					newUser := User{
						ID:    string(len(users) + 1),
						Name:  name,
						Email: email,
					}
					users = append(users, newUser)
					return newUser, nil
				},
			},
		},
	},
)

// Schema definition
var schema, _ = graphql.NewSchema(
	graphql.SchemaConfig{
		Query:    rootQuery,
		Mutation: rootMutation,
	},
)

func main() {
	// GraphQL handler
	h := handler.New(&handler.Config{
		Schema:   &schema,
		Pretty:   true,
		GraphiQL: true,
	})

	// Routes
	http.Handle("/graphql", h)
	http.HandleFunc("/health", healthHandler)

	log.Println("GraphQL server running on http://localhost:8080/graphql")
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"status": "healthy"})
}
