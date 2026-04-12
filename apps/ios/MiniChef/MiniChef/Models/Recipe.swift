//
//  Recipe.swift
//  MiniChef
//
//  Created by Nico Ricaldi on 4/11/26.
//

import Foundation
import SwiftData

@Model
class Recipe {
    var id = UUID()
    var title: String
    var desc: String
    var ingredients: [String]
    var steps: [String]

    init(title: String, desc: String, ingredients: [String] = [], steps: [String] = []) {
        self.title = title
        self.desc = desc
        self.ingredients = ingredients
        self.steps = steps
    }

    func isReady () -> Bool {
        return self.ingredients.isEmpty || self.steps.isEmpty
    }
}
